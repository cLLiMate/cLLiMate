resource "google_cloud_run_v2_service" "default" {
  for_each = toset(["live"])
  name     = "${local.project_id}-${each.key}"
  location = local.region

  template {
    scaling {
      max_instance_count = 20
    }
    containers {
      image = "${local.region}-docker.pkg.dev/${local.project_id}/${local.project_id}/site:${each.key}"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [google_project_service.default["run"]]
}

resource "google_cloud_run_v2_service" "api" {
  for_each = toset(["live"])
  name     = "${local.project_id}-api-${each.key}"
  location = local.region

  template {
    scaling {
      max_instance_count = 20
    }
    containers {
      image = "${local.region}-docker.pkg.dev/${local.project_id}/${local.project_id}/api:${each.key}"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [google_project_service.default["run"]]
}

resource "google_cloud_run_service_iam_member" "default-all-users" {
  for_each = toset(keys(google_cloud_run_v2_service.default))
  service  = google_cloud_run_v2_service.default[each.key].name
  location = google_cloud_run_v2_service.default[each.key].location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "api-all-users" {
  for_each = toset(keys(google_cloud_run_v2_service.api))
  service  = google_cloud_run_v2_service.api[each.key].name
  location = google_cloud_run_v2_service.api[each.key].location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = merge({
    for key in keys(google_cloud_run_v2_service.default) :
    key => google_cloud_run_v2_service.default[key].uri
  },
  {
    for key in keys(google_cloud_run_v2_service.api) :
    "api-${key}" => google_cloud_run_v2_service.api[key].uri
  })
}
