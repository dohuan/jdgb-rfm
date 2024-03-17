#!/bin/bash

set -e

source ./.env

export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
export GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA=${GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA}
export PROJECT_ID=${PROJECT_ID}
export REGION=${REGION}
export PROJECT_ID_awesome_company_DATA=${PROJECT_ID_awesome_company_DATA}

export GOOGLE_KEY_FILE_PATH_TERRAFORM=${GOOGLE_KEY_FILE_PATH_TERRAFORM}
export GOOGLE_KEY_FILE_PATH=${GOOGLE_KEY_FILE_PATH}
export GOOGLE_KEY_FILE_PATH_awesome_company_DATA=${GOOGLE_KEY_FILE_PATH_awesome_company_DATA}
export ENV_NAME=${ENV_NAME}
export DBT_USER=${DBT_USER}



# make build-local run-dbt-local



echo "Run Terraform"
export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_KEY_FILE_PATH_TERRAFORM}
cd deploy/terraform
# make ${ENV_NAME}-terraform-init ${ENV_NAME}-terraform-plan-destroy
make ${ENV_NAME}-terraform-init ${ENV_NAME}-terraform-plan-destroy ${ENV_NAME}-terraform-apply
# make ${ENV_NAME}-terraform-init ${ENV_NAME}-terraform-plan ${ENV_NAME}-terraform-apply
# cd ../../

# make build-cloud compile-vertex
# make compile-vertex
# make build-cloud deploy-cloud-run-invoker
# make deploy-dags

# python local-test.py
# make build-local run-local-invoker