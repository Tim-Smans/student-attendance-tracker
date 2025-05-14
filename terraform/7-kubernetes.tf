resource "google_container_cluster" "primary" {
  name                      = "primary"
  location                  = "europe-north1-a"
  remove_default_node_pool  = true
  initial_node_count        = 1
  network                   = google_compute_network.main.self_link
  subnetwork                = google_compute_subnetwork.private.self_link
  logging_service           = "logging.googleapis.com/kubernetes"
  networking_mode           = "VPC_NATIVE"
  deletion_protection = false

  lifecycle {
    ignore_changes = [initial_node_count]
  }

  node_locations = [
    "europe-north1-b"
  ]

  node_config {
    machine_type = "e2-medium"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }

  addons_config {
    http_load_balancing {
      disabled = true
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }

  release_channel {
    channel = "REGULAR"
  }

  workload_identity_config {
    workload_pool = "prj-mtp-aiot-aisk-sat.svc.id.goog"
  }

  ip_allocation_policy {
    cluster_secondary_range_name  = "k8s-pod-range"
    services_secondary_range_name = "k8s-service-range"
  }

  private_cluster_config {
    enable_private_nodes      = true
    enable_private_endpoint   = false
    master_ipv4_cidr_block    = "172.16.0.0/28"
  }

}