terraform {
  backend "gcs" {
    bucket = "cllimate-tfstate"
    prefix = "cllimate"
  }
}

locals {
  project_id = "cllimate"
  region     = "us-central1"
  repo_name  = "cLLiMate"
  owner      = "cLLiMate"
}

provider "google" {
  project = local.project_id
  region  = local.region
}

data "google_project" "project" {}

resource "google_project_service" "default" {
  for_each = toset([
    "compute",
    "artifactregistry",
    "run",
    "cloudbuild",
    "iam",
    "cloudkms",
    "secretmanager",
  ])
  service = "${each.key}.googleapis.com"
}

resource "google_artifact_registry_repository" "default" {
  location      = local.region
  repository_id = local.project_id
  format        = "DOCKER"
  depends_on    = [google_project_service.default["artifactregistry"]]
}

// get the compute engine default service account
data "google_compute_default_service_account" "default" {
  project = local.project_id
  depends_on = [google_project_service.default["compute"]]
}

// grant the compute engine default service account push access to the artifact registry
resource "google_artifact_registry_repository_iam_member" "default" {
  repository = google_artifact_registry_repository.default.name
  location   = google_artifact_registry_repository.default.location
  role       = "roles/artifactregistry.repoAdmin"
  member     = "serviceAccount:${data.google_compute_default_service_account.default.email}"
}

resource "google_storage_bucket" "default" {
  name     = local.project_id
  location = "US"
  versioning {
    enabled = true
  }
  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }
  cors {
    origin          = ["*"]
    method          = ["GET"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

resource "google_storage_bucket_iam_binding" "default-public" {
  bucket = google_storage_bucket.default.name
  role   = "roles/storage.objectViewer"
  members = [
    "allUsers"
  ]
}

output "bucket_name" {
  value = google_storage_bucket.default.name
}
