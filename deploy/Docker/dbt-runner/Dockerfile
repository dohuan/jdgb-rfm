FROM python:3.8

LABEL maintainer="Jay Do"

ARG GOOGLE_APPLICATION_CREDENTIALS
ARG PROJECT_ID
ARG ENV_NAME
ARG DBT_USER

ENV TZ=Australia/Sydney
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
ENV PROJECT_ID=$PROJECT_ID
ENV ENV_NAME=$ENV_NAME
ENV DBT_USER=$DBT_USER

RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
  git libpq-dev python-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update && \
  apt-get install --no-install-recommends -y -q sqlformat


RUN mkdir dbt
COPY dbt/ /dbt
WORKDIR /dbt

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN echo ${GOOGLE_APPLICATION_CREDENTIALS} | base64 -d > ./gcloud-api-key.json

CMD ["bash"]