resource "google_service_account" "composer" {
  account_id   = "composer-sa"
  display_name = "composer default"
  description  = "Used by the Composer RFM."
}

resource "google_service_account_iam_member" "custom_service_account" {
  provider           = google-beta
  service_account_id = google_service_account.composer.id
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:service-${data.google_project.awesome_company_datascience_rfm.number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_composer_environment" "rfm_controller" {
  provider = google-beta
  name     = "rfm-controller"
  region   = var.region
  labels   = {}

  config {
    node_config {
      service_account = google_service_account.composer.name
      network         = google_compute_network.rfm_network.id
    }

    software_config {
      image_version = "composer-2.0.27-airflow-2.2.5"

      airflow_config_overrides = {
        core-dags_are_paused_at_creation      = "False"
        core-max_active_runs_per_dag          = "15"
        core-enable_xcom_pickling             = "True"
        webserver-hide_paused_dags_by_default = "True"
        api-auth_backend                      = "airflow.api.auth.backend.default"
      }

      pypi_packages = {
        pymssql  = "<3.0"
        olefile  = "==0.46"
        openpyxl = "==3.0.7"
        pydrive  = "==1.3.1"
      }

      env_variables = {
        CLOUD_COMPOSER = "true"
      }
    }
  }

  depends_on = [
    google_project_iam_member.composer_sa_roles,
    google_compute_network.rfm_network
  ]
}


resource "google_compute_network" "rfm_network" {
  name = "composer-network"
}

resource "google_project_iam_member" "composer_sa_roles" {
  for_each = toset([
    "roles/composer.worker",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber",
    "roles/cloudfunctions.developer",
    "roles/run.developer"
  ])
  role    = each.key
  member  = "serviceAccount:${google_service_account.composer.email}"
  project = var.project_id
}
