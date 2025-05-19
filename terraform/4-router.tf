/*
  This is a virtual router that supports Border Gateway protocol, important for Cloud NAT
*/

resource "google_compute_router" "router" {
  name      = "router"
  region    = "europe-north1"
  network   = google_compute_network.main.id
  
}