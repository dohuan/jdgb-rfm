terraform {
  backend "gcs" {}
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

data "google_project" "awesome_company_datascience_rfm" {
}


resource "google_service_account" "service_account_vertex_ai" {
  account_id   = "service-account-vertex-ai"
  display_name = "Vertex AI Service Account"
  description  = "Service account used by Vertex AI."
}

resource "google_project_iam_member" "service_account_vertex_ai_roles" {
  for_each = toset([
    "roles/aiplatform.admin",
    "roles/bigquery.admin",
    "roles/storage.admin",
    "roles/cloudbuild.builds.editor",
    "roles/run.developer",
    "roles/cloudfunctions.developer",
    "roles/cloudscheduler.admin",
    "roles/iam.serviceAccountUser",
    "roles/composer.environmentAndStorageObjectAdmin",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber"
  ])
  role    = each.key
  member  = "serviceAccount:${google_service_account.service_account_vertex_ai.email}"
  project = var.project_id
}

resource "google_project_iam_member" "vertex_ai_service_agent_roles" {
  for_each = toset([
    "roles/artifactregistry.reader"
  ])
  role    = each.key
  member  = "serviceAccount:service-${data.google_project.awesome_company_datascience_rfm.number}@gcp-sa-aiplatform-cc.iam.gserviceaccount.com"
  project = var.project_id
}


resource "google_storage_bucket" "gcs_vertex_ai" {
  name          = "${var.project_id}-vertex-ai"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_pubsub_topic" "rfm_controller_topic" {
  name = "rfm-controller"
} # topic for passing controller signals from/to Airflow

resource "google_pubsub_subscription" "rfm_controller_pull_subscription" {
  name  = "rfm-controller-pull-subscription"
  topic = google_pubsub_topic.rfm_controller_topic.name

  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = false

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "1296000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = false
}