/*
  Creating a dedicated GCP service account for the nodes.
*/
resource "google_service_account" "kubernetes" {
  account_id = "kubernetes"
}

/*
  This is our general node pool
    Node Count = One node in this pool, no autoscaling
    Machine type = Budget friendly machine type
    Autorepair & Autoupgrade = Keeps node up to date and healthy
    Service Account = Connects our own service account
    Labels.Role = Handy for selection via NodeSelector in our pods
*/
resource "google_container_node_pool" "general" {
  name        = "general"
  cluster     = google_container_cluster.primary.id
  node_count  = 1

  management {
    auto_repair   = true
    auto_upgrade  = true
  }

  node_config {
    preemptible   = false
    machine_type  = "e2-small"

    labels = {
      role = "general"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

/*
  This is our preemptible node pool (spot pool)
    Preemptible = Costs less, can be spun down at any moment.
    Autoscaling = Dynamic from 0 -> 5 nodes
    Taint = Prevents normal pods to run here, except they are using 'tolerations'
*/
resource "google_container_node_pool" "spot" {
  name    = "spot"
  cluster     = google_container_cluster.primary.id

  management {
    auto_repair   = true
    auto_upgrade  = true
  }

  autoscaling {
    min_node_count = 0
    max_node_count = 5
  }

  node_config {
    preemptible   = true
    machine_type  = "e2-small"

    labels = {
      role = "spot"
    }

    taint {
      key     = "instance_type"
      value   = "spot"
      effect  = "NO_SCHEDULE"
    }

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }

    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}