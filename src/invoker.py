import os

from src.pipeline import get_pipeline
from kfp.v2 import compiler
from kfp.v2.google.client import AIPlatformClient
from google.oauth2 import service_account
from datetime import datetime

from src.helper.helper import upload_blob


def run(dbt_run_date: str):
    """
    This function to be used with design that uses Cloud Func as invoker
    The compiled pipeline.json is built in CICD, hence can not pass run-time
    parameters.
    """
    PROJECT_ID = os.environ.get("PROJECT_ID")
    compiler.Compiler().compile(
        pipeline_func=get_pipeline(
            pipeline_name="rfm",
            base_image="gcr.io/{}/rfm:latest".format(PROJECT_ID),
            dbt_run_date=dbt_run_date
        ),
        package_path='pipeline.json',
        type_check=False
    )

    creds = service_account.Credentials.from_service_account_file(
        "./gcloud-api-key.json"
    )
    if_uploaded = upload_blob(
        "{}-vertex-ai".format(PROJECT_ID),
        "pipeline.json",
        "pipeline.json",
        creds
    )

    if if_uploaded == True:
        out = "Compiled file uploaded."
    else:
        out = "ERROR: Compiled file failed to upload."
    return out


def invoke(
    dbt_run_date: str
):
    """
    This function to be used with design that uses Cloud Run as invoker, the compiling
    and submitting are done in a same call, hence it is possible to pass run-time
    parameters.
    """
    PROJECT_ID = os.environ.get("PROJECT_ID")
    compiler.Compiler().compile(
        pipeline_func=get_pipeline(
            pipeline_name="rfm",
            base_image="gcr.io/{}/rfm:latest".format(PROJECT_ID),
            dbt_run_date=dbt_run_date
        ),
        package_path='pipeline.json',
        type_check=False
    )
    vertex_ai_client = AIPlatformClient(
        project_id=PROJECT_ID,
        region="us-central1"
    )

    response = vertex_ai_client.create_run_from_job_spec(
        job_id="rfm-{}".format(datetime.now().strftime("%Y%M%d%H%m%S")),
        job_spec_path="pipeline.json",
        pipeline_root="gs://{}-vertex-ai".format(PROJECT_ID),
        enable_caching=False,
        service_account="service-account-vertex-ai@{}.iam.gserviceaccount.com".format(
            PROJECT_ID)
    )
    out = "displayName: {}, created: {}, state: {}".format(
        response['displayName'],
        response['createTime'],
        response['state']
    )
    return out


if __name__ == '__main__':
    print(run("2022-09-29"))
