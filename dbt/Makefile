define DBT_VARS_YAML
{
	project_id: ${PROJECT_ID},
	dataset: ${DBT_USER},
	run_date: ${RUN_DATE}
}
endef

DBT_VARS := $(shell echo "${DBT_VARS_YAML}" | sed -e "s/\t//g" -z)

run:  # this is NOT used in pipeline
	dbt run --profiles-dir . --vars "${DBT_VARS}"

run-full-refresh:
	dbt run --profiles-dir . --vars "${DBT_VARS}" --full-refresh

run-docs:
	echo "Generating dbt lineage graph, wait 10 seconds before hitting the link."
	dbt docs generate --profiles-dir . --vars "${DBT_VARS}"
	dbt docs serve --profiles-dir . --vars "${DBT_VARS}"
