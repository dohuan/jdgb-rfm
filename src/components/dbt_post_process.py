from typing import NamedTuple


def dbt_post_process(
    run_date: str
) -> NamedTuple(
        'runStatus', [
            ('ifSuccess', str)
        ]
):
    import os
    from collections import namedtuple
    from google.oauth2 import service_account
    from src.helper.helper import send_msg_to_pubsub

    creds = service_account.Credentials.from_service_account_file(
        os.environ.get("GOOGLE_KEY_FILE_PATH"))
    out = send_msg_to_pubsub(
        "rfm-controller",
        credential=creds,
        message={"run_date": run_date, "status": "success"}
    )
    run_output = namedtuple('runStatus', ['ifSuccess'])
    return run_output(str(out))
