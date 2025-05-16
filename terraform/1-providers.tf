provider "google" {
  project = "prj-mtp-aiot-aisk-sat"
  region  = "europe-north1"
}

//Create this bucket before applying terraform
terraform {
  backend "gcs" {
    bucket = "timsmans-tf-state-staging"
    prefix = "terraform/state"
  }
  
}


data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = google_container_cluster.primary.endpoint
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  token                  = data.google_client_config.default.access_token
}


provider "helm" {
  kubernetes {
    host                   = google_container_cluster.primary.endpoint
    cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
    token                  = data.google_client_config.default.access_token
  }
}