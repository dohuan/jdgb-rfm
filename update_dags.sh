#!/bin/bash

for file in src/dags/*.py; do
    echo "Uploading ${file}"
    gcloud composer environments storage dags import \
        --source ${file} \
        --environment "rfm-controller" \
        --location ${REGION}
done

echo "Update env vars in Composer"
RUN_URL=$(gcloud run services describe rfm-vertex-ai-invoker --platform managed --region ${REGION} --format 'value(status.url)')
echo "RUN_URL=${RUN_URL}"
gcloud composer environments update "rfm-controller" \
              --location ${REGION} \
              --update-env-variables=REGION=${REGION},CLOUD_RUN_URL=${RUN_URL}