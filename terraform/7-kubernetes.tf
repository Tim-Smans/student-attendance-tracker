resource "google_container_cluster" "primary" {
  /*
    Creating the Kubernetes Cluster
      Location = Setting up the cluster inside of one zone (Zonal cluster)
      Remove Default Node Pool & Initial Node Count = Deletes the standard node pool, gives us complete control 
      over the nodes. 
      Network & Subnetwork & Networking mode = Connects cluster to custom VPC and subnet.

  */

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

  /*
    Configure your nodes
      Machine type = the machine that your cluster will run on, e2-medium is great for dev/test workloads,
                     this has a huge impact on the pricing.
      Secure boot = Prevents boot level malware
      Integrity Monitoring = Detects changes to the VM during runtime
  */

  node_config {
    machine_type = "e2-medium"

    shielded_instance_config {
      enable_secure_boot          = true
      enable_integrity_monitoring = true
    }
  }

  /*
    We disable L7 Load balancing via GKE ingress controller. We will be using NGINX ourselves.
    We enable autoscaling on pods.
  */
  addons_config {
    http_load_balancing {
      disabled = true
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }

  /*
    We choose the 'stable' release channel
  */
  release_channel {
    channel = "REGULAR"
  }

  /*
    Connects our kubernetes service accounts to IAM using Workload identity.
  */
  workload_identity_config {
    workload_pool = "prj-mtp-aiot-aisk-sat.svc.id.goog"
  }

  /*
    Links our secondary IP ranges from our subnet for the pods and services.
  */
  ip_allocation_policy {
    cluster_secondary_range_name  = "k8s-pod-range"
    services_secondary_range_name = "k8s-service-range"
  }

  /*
    Private nodes = No public Ip's good for security
    Privare endpoint false = Means the Kubernetes API is also publically accessabble (with auth)
  */
  private_cluster_config {
    enable_private_nodes      = true
    enable_private_endpoint   = false
    master_ipv4_cidr_block    = "172.16.0.0/28"
  }

}