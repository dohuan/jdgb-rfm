FROM python:3.8

LABEL maintainer="Jay Do"

ARG GOOGLE_APPLICATION_CREDENTIALS
ARG GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA
ARG PROJECT_ID
ARG PROJECT_ID_awesome_company_DATA
ARG ENV_NAME

ENV TZ=Australia/Sydney
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
ENV GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA=$GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA
ENV PROJECT_ID=$PROJECT_ID
ENV PROJECT_ID_awesome_company_DATA=$PROJECT_ID_awesome_company_DATA
ENV ENV_NAME=$ENV_NAME

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip libgomp1 libc-dev build-essential curl gcc libffi-dev make
RUN pip install -U pip

WORKDIR app
RUN echo ${GOOGLE_APPLICATION_CREDENTIALS} | base64 -d > ./gcloud-api-key.json
RUN echo ${GOOGLE_APPLICATION_CREDENTIALS_awesome_company_DATA} | base64 -d > ./gcloud-api-key-awesome_company-data.json
COPY . .

ENV GOOGLE_KEY_FILE_PATH=./gcloud-api-key.json
ENV GOOGLE_KEY_FILE_PATH_awesome_company_DATA=./gcloud-api-key-awesome_company-data.json

RUN pip install -r requirements.txt

RUN python setup.py bdist_wheel
RUN pip install dist/src-0.0.1-py3-none-any.whl
