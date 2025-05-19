/*
  Enable GCP Api's
    Compute is essential for networks, firewalls and VM's
*/
resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
}

/*
  Enable GCP Api's
    Container is essential for creating Kubernetes clusters.
*/
resource "google_project_service" "container" {
  service = "container.googleapis.com"
}

/*
  This will create a custom VPC network, giving you detailed control.
    Name = Name of the VPC
    Routing mode = "REGIONAL" = Only traffic inside of the region stays intern, Traffic between different regions goes over internet.
    Auto Create Subnetworks = Makes  sure GCP doesn't automatically create subnets.
    mtu = 'Maximum transmission unit' - Standards for GCP
    Delete default routes on create = Leaves the standard routes (0.0.0.0), so traffic to the outside stays possible.
    Depends on = Makes sure this is only executed after the required API's are available 
*/
resource "google_compute_network" "main" {
  name                              = "main"
  routing_mode                      = "REGIONAL"
  auto_create_subnetworks           = false
  mtu                               = 1460
  delete_default_routes_on_create   = false

  depends_on = [
    google_project_service.compute,
    google_project_service.container
  ]
}