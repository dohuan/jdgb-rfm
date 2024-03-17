IMAGE_NAME_DBT_RUNNER=gcr.io/${PROJECT_ID}/rfm-dbt-runner
IMAGE_NAME_INVOKER=gcr.io/${PROJECT_ID}/rfm-vai-invoker
IMAGE_NAME_RFM=gcr.io/${PROJECT_ID}/rfm
FUNC_URL=https://${REGION}-${PROJECT_ID}.cloudfunctions.net/rfm-dbt-runner-func
VERTEX_PIPELINE_BUCKET=${PROJECT_ID}-vertex-ai
TAG=latest


build-local:
	docker build -f deploy/Docker/dbt-runner/Dockerfile \
		--build-arg GOOGLE_APPLICATION_CREDENTIALS \
		--build-arg PROJECT_ID \
		--build-arg DBT_USER \
		-t ${IMAGE_NAME_DBT_RUNNER}:${TAG} .

	docker build -f deploy/Docker/invoker/Dockerfile \
		--build-arg GOOGLE_APPLICATION_CREDENTIALS \
		--build-arg PROJECT_ID \
		-t ${IMAGE_NAME_INVOKER}:${TAG} .

run-local-invoker:
	docker run -p 8080:8080 -e PORT=8080 ${IMAGE_NAME_INVOKER}:${TAG}

run-dbt-local:
	docker run -it --mount type=bind,source=$(shell pwd)/dbt,target=/local/dbt \
		-p 8080:8080 \
		${IMAGE_NAME_DBT_RUNNER}:${TAG}

build-cloud:


	gcloud builds submit \
		--project=${PROJECT_ID} \
		--config=cloudbuild_dbt_runner.yaml \
		--substitutions=_GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}",_PROJECT_ID="${PROJECT_ID}",_DBT_USER="${DBT_USER}",_IMAGE_NAME_DBT_RUNNER="${IMAGE_NAME_DBT_RUNNER}",_TAG="${TAG}" \
		.

	gcloud builds submit \
		--project=${PROJECT_ID} \
		--config=cloudbuild_invoker.yaml \
		--substitutions=_GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}",_PROJECT_ID="${PROJECT_ID}",_IMAGE_NAME_INVOKER="${IMAGE_NAME_INVOKER}",_TAG="${TAG}" \
		.

	gcloud builds submit \
		--project=${PROJECT_ID} \
		--config=cloudbuild_rfm.yaml \
		--substitutions=_GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}",_GOOGLE_APPLICATION_CREDENTIALS_AWESOME_COMPANY_DATA="${GOOGLE_APPLICATION_CREDENTIALS_AWESOME_COMPANY_DATA}",_PROJECT_ID="${PROJECT_ID}",_PROJECT_ID_AWESOME_COMPANY_DATA="${PROJECT_ID_AWESOME_COMPANY_DATA}",_ENV_NAME="${ENV_NAME}",_IMAGE_NAME_RFM="${IMAGE_NAME_RFM}",_TAG="${TAG}"\
		.

deploy-cloud-run-invoker:
	gcloud run deploy rfm-vertex-ai-invoker \
		--platform managed \
		--region ${REGION} \
		--image ${IMAGE_NAME_INVOKER} \
		--no-allow-unauthenticated \
		--service-account service-account-vertex-ai@${PROJECT_ID}.iam.gserviceaccount.com

deploy-dags:
	./update_dags.sh
