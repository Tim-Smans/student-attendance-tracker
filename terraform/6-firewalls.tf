/*
  Defining the Cloud firewall rule
  This allows SSH traffic to all VM's inside of our VPC
    Network = Points to our VPC
    Allow.Protocol = Allows TCP (Neceserry for SSH)
    Allow.Ports = 22 is standard for SSH
    Source Ranges = All IP-adresses worldwide.
*/

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.main.name


  allow {
    protocol  = "tcp"
    ports     = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}