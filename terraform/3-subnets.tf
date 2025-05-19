/*
  This defines a custom subnet inside of our earlier created VPC.
    Base configuration:
      Name = Name of the subet, visisble in GCP Console
      Ip Cidr Range = IP-Range for VM's and nodes (16.384 ip's)
      Region = Needs to be the same as the region of the VPC and cluster
      Network = Points to your earlier created VPC 'main'
      Private Ip Google Access = Allows resources without a public ip to connect to google API's
    Secondary Ip Ranges:
      These are specific to GKE with VPC-native clusters
      k8s-pod-range = Ip's that are used for the pods, every pod gets an ip from this pool.
      k8s-service-range = Ip's for the CLusterIP services within the Kubernetes cluster
      Make sure these ranges don't overlap!
*/

resource "google_compute_subnetwork" "private"{
  name                      = "private"
  ip_cidr_range             = "10.0.0.0/18"
  region                    = "europe-north1"
  network                   = google_compute_network.main.id
  private_ip_google_access  = true

  secondary_ip_range {
    range_name    = "k8s-pod-range"
    ip_cidr_range = "10.48.0.0/14"
  }

  secondary_ip_range {
    range_name    = "k8s-service-range"
    ip_cidr_range = "10.52.0.0/20"
  }
 
}