
/*
  Connects to google cloud
    Project = The project id where we want to create the resources.
    Region = The region where the resources are set up.
*/
provider "google" {
  project = "prj-mtp-aiot-aisk-sat"
  region  = "europe-north1"
}

/*
  Saves the terraform state file inside of a Google Cloud Storage bucket.
  This is important for remote state management. If users on 2 different pc's are updating the terraform setup and
  applying it, they always have the latest state of the Google Cloud.
    Bucket = The name of the bucket we are saving the state in (make sure to create this bucket before terraform init)
    Prefix = The File / Directory path
*/
terraform {
  backend "gcs" {
    bucket = "timsmans-tf-state-staging"
    prefix = "terraform/state"
  }
  
}


/*
  Retrieves the local authentication, like tokens, project, region...
  Is later used to give Kubernetes and Helm access to the GKE cluster.
*/
data "google_client_config" "default" {}

/*
  Allows terraform to work with your Kubernetes Cluster
    Host = The public endpoint (API server) of your GKE cluster
    Cluster Ca Certificate = Needs this CA cert of the cluster to setup HTTPS connections
    Token = Is a bearer token for authentication, retrieved from local gcloud login.
*/
provider "kubernetes" {
  host                   = google_container_cluster.primary.endpoint
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
  token                  = data.google_client_config.default.access_token
}



/*
  This allows Helm to deploy charts to your GKE cluster
    It takes the same parameters as the kubernetes provider
*/
provider "helm" {
  kubernetes {
    host                   = google_container_cluster.primary.endpoint
    cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
    token                  = data.google_client_config.default.access_token
  }
}