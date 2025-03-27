provider "google" {
  project = var.gcp_project
  region  = var.region
}

resource "google_storage_bucket" "healthvision_data" {
  name          = "${var.gcp_project}-healthvision-data"
  location      = var.region
  force_destroy = false
  uniform_bucket_level_access = true
}

resource "google_pubsub_topic" "image_processed" {
  name = "image-processed"
}

resource "google_vertex_ai_dataset" "ultrasound" {
  display_name        = "ultrasound-dataset"
  metadata_schema_uri = "gs://google-cloud-aiplatform/schema/dataset/metadata/image_1.0.0.yaml"
  region             = var.region
}

resource "google_service_account" "ml_service" {
  account_id   = "ml-service-account"
  display_name = "ML Service Account"
}

resource "google_project_iam_member" "ml_service_ai" {
  project = var.gcp_project
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ml_service.email}"
}

resource "google_kubernetes_cluster" "healthvision_cluster" {
  name     = "healthvision-cluster"
  location = var.region
  initial_node_count = 2

  node_config {
    machine_type = "e2-medium"
    service_account = google_service_account.ml_service.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}