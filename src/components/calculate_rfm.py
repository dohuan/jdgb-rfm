from typing import NamedTuple


def calculate_rfm(
    bq_dataset: str,
    bq_table: str
) -> NamedTuple(
        'runStatus', [
            ('ifSuccess', str)
        ]
):
    import os
    from collections import namedtuple
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound
    from google.oauth2 import service_account
    from src.helper.helper import upload_to_bq

    cred_algo = service_account.Credentials.from_service_account_file(
        os.environ.get("GOOGLE_KEY_FILE_PATH"))
    cred_data = service_account.Credentials.from_service_account_file(
        os.environ.get("GOOGLE_KEY_FILE_PATH_awesome_company_DATA"))

    bqclient = bigquery.Client(credentials=cred_algo)
    bq_query = """
        select * from {}.{}
    """.format(bq_dataset, bq_table)

    df = (
        bqclient.query(bq_query)
        .result()
        .to_dataframe(create_bqstorage_client=True)
    )
    df = df[[
        'order_nr',
        'id_customer',
        'payment_method',
        'sales_br'
    ]]
    env_name = os.environ.get("ENV_NAME")
    if env_name != "prod":
        output_table_name = "rfm-{}".format(env_name)
    else:
        output_table_name = "rfm"
    dest_schema = {
        "project_id": os.environ.get("PROJECT_ID_awesome_company_DATA"),
        "dataset": "mlops_mkt",
        "table": output_table_name,
        "schema": [
            {"name": "order_nr", "type": "STRING"},
            {"name": "id_customer", "type": "STRING"},
            {"name": "payment_method", "type": "STRING"},
            {"name": "sales_br", "type": "FLOAT"}
        ]
    }
    out = upload_to_bq(
        df,
        dest_schema,
        cred_data
    )
    run_output = namedtuple('runStatus', ['ifSuccess'])
    return run_output(str(out))


if __name__ == '__main__':
    calculate_rfm(
        'biz_rfm',
        'rfm'
    )
