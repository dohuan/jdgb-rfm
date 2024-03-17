import os
from datetime import datetime
from datetime import timedelta
from httplib2 import Credentials
from pandas_gbq.gbq import InvalidSchema
from google.cloud import storage
from google.cloud import pubsub_v1


def upload_to_bq(data, destination_info, credential, isexists="append"):
    success = True
    try:
        data.to_gbq(
            project_id=destination_info["project_id"],
            destination_table=destination_info["dataset"]
            + "."
            + destination_info["table"],
            credentials=credential,
            if_exists=isexists,
            table_schema=destination_info["schema"],
        )
    except InvalidSchema:
        # LOGGER.error("Invalid Schema error. (muted)")
        success = False
    return success


def send_msg_to_pubsub(
    topic,
    credential,
    message: dict
):
    publisher = pubsub_v1.PublisherClient(credentials=credential)
    msg_package = bytes(str(message), encoding="utf-8")
    topic_name = "projects/{project_id}/topics/{topic}".format(
        project_id=os.environ.get("PROJECT_ID"), topic=topic
    )
    future = publisher.publish(
        topic_name,
        msg_package
    )
    return future.result()


def download_blob(bucket_name, source_blob_name, destination_file_name, credentials):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print("Blob {} downloaded to {}.".format(
        source_blob_name, destination_file_name))


def upload_blob(bucket_name, source_file_name, destination_blob_name, credentials):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
    return True


def list_blobs(bucket_name, credentials):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(credentials=credentials)
    blobs = storage_client.list_blobs(bucket_name)
    return [blob.name for blob in blobs]


def delete_blob(bucket_name, blob_name, credentials):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print("Blob {} deleted.".format(blob_name))


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
