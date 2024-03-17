FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

LABEL maintainer="tech.data.datascience@awesome_company.com.au"

ARG GOOGLE_APPLICATION_CREDENTIALS
ARG PROJECT_ID

ENV TZ=Australia/Sydney
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
ENV PROJECT_ID=$PROJECT_ID

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip libgomp1 libc-dev build-essential curl gcc libffi-dev make
RUN pip install -U pip

WORKDIR app
RUN echo ${GOOGLE_APPLICATION_CREDENTIALS} | base64 -d > ./gcloud-api-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=./gcloud-api-key.json
COPY . .

RUN pip install -r src/app_invoker/requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.app_invoker.app:app