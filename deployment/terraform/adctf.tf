provider "google" {
    credentials = file("account.json")
    project = "inctf-international-2020"
    region  = "us-central1-a" 
}

resource "google_compute_firewall" "wireguard" {
 name    = "wireguard"
 network = "default"

 allow {
   protocol = "udp"
   ports    = ["51820"]
 }
}

resource "google_compute_firewall" "openvpn" {
 name    = "openvpn"
 network = "default"

 allow {
   protocol = "udp"
   ports    = ["1194"]
 }
}

resource "google_compute_instance" "router" {
 name         = "router-vm"
 machine_type = "n1-highcpu-2"
 zone         = "us-central1-a"

 tags = ["wireguard"]
 boot_disk {
   initialize_params {
     image = "ubuntu-2004-focal-v20200729"
   }
 }
 network_interface {
   network = "default"

   access_config {
     // Include this section to give the VM an external ip address
   }
 }

metadata = {
   ssh-keys = "friday:${file("~/.ssh/id_rsa.pub")}"
}
}

 output "router-ip" {
  value = google_compute_instance.router.network_interface.0.access_config.0.nat_ip
}


resource "google_compute_instance" "team" {
 count = 2
 name         = "team-${count.index + 1}"
 machine_type = "n1-highcpu-2"
 zone         = "us-central1-a"

 tags = ["wireguard", "openvpn"]
 boot_disk {
   initialize_params {
     image = "ubuntu-2004-focal-v20200729"
   }
 }
 network_interface {
   network = "default"

   access_config {
     // Include this section to give the VM an external ip address
   }
 }

metadata = {
   ssh-keys = "friday:${file("~/.ssh/id_rsa.pub")}"
}
}

output "team-ip" {
    value = google_compute_instance.team.*.network_interface.0.access_config.0.nat_ip
}