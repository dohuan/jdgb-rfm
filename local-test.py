import os
from src.helper.helper import send_msg_to_pubsub
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file(
    os.environ.get("GOOGLE_KEY_FILE_PATH")        
)

print(
    send_msg_to_pubsub(
        "rfm-controller",
        credential=creds,
        message={"run_date": "2022-09-29", "status": "success"}
    )
)

