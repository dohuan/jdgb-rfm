from distutils.log import error
import os
import urllib
import base64
import json
from datetime import datetime, timedelta
import pendulum
import requests

import google.auth.transport.requests
import google.oauth2.id_token

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.utils.email import send_email
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.sensors.pubsub import PubSubPullSensor


TZ = "Australia/Sydney"


def get_monday_this_week():
    now = datetime.now().date()
    now = datetime.combine(now, datetime.min.time())
    monday = now - timedelta(days=now.weekday())  # Monday of this week
    return monday


def get_last_sunday():
    now = datetime.now().date()
    now = datetime.combine(now, datetime.min.time())
    sunday = now - timedelta(days=now.weekday() + 1)  # Last Sunday
    return sunday


def get_last_saturday():
    now = datetime.now().date()
    now = datetime.combine(now, datetime.min.time())
    saturday = now - timedelta(days=now.weekday() + 1)  # Last Saturday
    return saturday


def send_request_to_dbt(dbt_model):
    r = requests.post(
        url='http://' + os.environ.get("DBTRUNNER_SERVICE_IP"),
        headers={"Content-Type": "application/json"},
        data=dbt_model,
    )
    print("response = {}".format(r.text))
    if "Completed successfully" not in r.text:
        raise ValueError("Sent request failed.")


def make_authorized_get_request(run_date):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """

    # Cloud Run uses your service's hostname as the `audience` value
    # audience = 'https://my-cloud-run-service.run.app/'
    # For Cloud Run, `endpoint` is the URL (hostname + path) receiving the request
    # endpoint = 'https://my-cloud-run-service.run.app/my/awesome/url'

    audience = os.environ.get("CLOUD_RUN_URL")
    endpoint = audience + "/invoke?run_date={}".format(run_date)
    req = urllib.request.Request(endpoint)
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response.read().decode('utf-8')


def pubsub_message_process(package, run_date):
    print("DEBUG")
    print(type(package))
    print(package)
    message = json.loads(
        base64.b64decode(package["message"]["data"]).decode(
            "utf-8").replace('\'', '\"')
    )
    print(message)
    print(run_date)
    if (message["run_date"] == run_date) & (message["status"] == 'success'):
        return {"task_status": "success"}
    else:
        return {"task_status": "failed"}


def check_task_status(ti, run_date):
    messages = ti.xcom_pull(key='return_value', task_ids='pubsub_sensor')
    any_success = False

    for msg in messages:
        status = pubsub_message_process(msg, run_date)
        if status["task_status"] == "success":
            any_success = True

    if any_success == False:
        raise ValueError("Task failed!")


default_args = {
    "owner": "tech.data.datascience@awesome_company.com.au",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "email": ["jay.do@awesome_company.com.au"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": True
}

dag = DAG(
    "rfm-dbt-runner",
    default_args=default_args,
    description="Run dbt model that feeds RFM",
    schedule_interval="0 8 * * 1",
    is_paused_upon_creation=True,
    start_date=pendulum.datetime(2022, 1, 1, tz=TZ),
    max_active_runs=1
)

s = DummyOperator(task_id="start", dag=dag)


t1 = PythonOperator(
    task_id="trigger_dbt_runner",
    python_callable=make_authorized_get_request,
    op_kwargs={'run_date': "{{ ds }}"},
    dag=dag,
)

t2 = PubSubPullSensor(
    task_id="pubsub_sensor",
    execution_timeout=timedelta(seconds=600),  # timeout after 10 min
    project_id=os.environ.get("PROJECT_ID"),
    subscription="rfm-controller-pull-subscription",
    max_messages=1,
    ack_messages=True
)

t3 = PythonOperator(
    task_id="check_task_status",
    python_callable=check_task_status,
    op_kwargs={'run_date': "{{ ds }}"},
    dag=dag
)

e = DummyOperator(task_id="end", dag=dag)

s >> t1 >> t2 >> t3 >> e
