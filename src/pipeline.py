import os
from kfp import components, dsl
from kfp.components import func_to_container_op
from src.components.dbt_post_process import dbt_post_process


def get_pipeline(
    pipeline_name,
    base_image,
    dbt_run_date
):
    if pipeline_name == "rfm":
        PROJECT_ID = os.environ.get("PROJECT_ID")
        DBT_USER = "main"
        DBT_IMAGE = "gcr.io/{}/rfm-dbt-runner:latest".format(PROJECT_ID)
        with open("src/components/component_dbt.yml", "r") as f:
            dbt_com_text = f.read()

        con_dbt = components.load_component_from_text(
            dbt_com_text.format(
                dbt_image=DBT_IMAGE,
                project_id=PROJECT_ID,
                dbt_user=DBT_USER,
                dbt_run_date=dbt_run_date
            )
        )

        con_dbt_post_process_op = func_to_container_op(
            dbt_post_process, base_image=base_image)

        @dsl.pipeline(
            name="calculate-rfm",
            description="Calculate RFM and upload to awesome-company-data"
        )
        def update_rfm():
            task_run_dbt = con_dbt().set_memory_request('3G')
            task_dbt_post = con_dbt_post_process_op(
                run_date=dbt_run_date
            ).set_memory_request('1G').after(task_run_dbt)

        return update_rfm

    else:
        return None
