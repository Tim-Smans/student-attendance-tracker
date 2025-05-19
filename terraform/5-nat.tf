/*
  We are creating a Cloud NAT (Network Address Translation) configuration, it is connected with the created router.
    Base configuration:
      Connects NAT to our existing Cloud Router inside of the same region.
    
    Subnet configuration:
      Sourse Subnetwork Ip Ranges to NAT = Means that we will be giving explicit subnetworks to NAT

    Subnetwork:
      NAT will be applied to all IP-ranges inside of the private subnet. 
      Makes sure that all outgoing requests from the subnet, go via NAT.

    Nat Ips:
      Coupling our self-made static external IP adress. 
*/

resource "google_compute_router_nat" "nat" {
  name    = "nat"
  router  = google_compute_router.router.name
  region  = "europe-north1"

  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  nat_ip_allocate_option             = "MANUAL_ONLY"

  subnetwork {
    name                    = google_compute_subnetwork.private.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  nat_ips = [google_compute_address.nat.self_link]
}

/*
  Creates an external, static IP adress, it is used by the NAT gateway.
  Using the Premium tier, it has low latency and google's fast backbone.
*/

resource "google_compute_address" "nat" {
  name          = "nat"
  address_type  = "EXTERNAL"
  network_tier  = "PREMIUM"

  depends_on = [google_project_service.compute]
}