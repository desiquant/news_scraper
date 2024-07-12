terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
    }
  }
}

# vars

variable "hetzner_token" {
  type        = string
  description = "hetzner cloud access token"
}

variable "server_id" {
  type        = string
  description = "hetzner cloud server id"
}

variable "floating_ips_count" {
  type        = number
  description = "total number of floating ips"
}

# used to trigger attaching existing ips to server
variable "dummy_trigger" {
  type        = string
  description = "attaching existing ips to server"
}

# existing resources

provider "hcloud" {
  token = var.hetzner_token
}


data "hcloud_server" "server" {
  id = var.server_id
}

# create floating ips and attach

resource "hcloud_floating_ip" "floating_ip" {
  count     = var.floating_ips_count
  type      = "ipv4"
  server_id = data.hcloud_server.server.id
}


resource "null_resource" "configure_ip" {
  depends_on = [hcloud_floating_ip.floating_ip]
  count      = length(hcloud_floating_ip.floating_ip)

  triggers = {
    server_ip     = data.hcloud_server.server.ipv4_address
    floating_ip   = hcloud_floating_ip.floating_ip[count.index].ip_address
    dummy_trigger = var.dummy_trigger
  }

  connection {
    type  = "ssh"
    user  = "root"
    host  = data.hcloud_server.server.ipv4_address
    agent = true
  }

  provisioner "remote-exec" {
    # NOTE: the ips are attached only till next reboot. to permanently configure: https://docs.hetzner.com/cloud/floating-ips/faq
    # TODO: it is looping over multiple ssh connection, instead maintain a single ssh connection and loop over commands.
    inline = [
      "sudo ip addr add ${hcloud_floating_ip.floating_ip[count.index].ip_address}/32 dev eth0",
      "echo 'Attached IPs:'",
      "ip addr show eth0 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"
    ]
  }

  # TODO: implement clean up on server by removing attached ips
  # provisioner "remote-exec" {
  #   when = destroy

  #   inline = [
  #     "sudo ip addr del ${self.triggers.floating_ip}/32 dev eth0",
  #     "ip addr show eth0 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"
  #   ]
  # }
}

# output all the attached ips
output "floating_ips" {
  value = hcloud_floating_ip.floating_ip.*.ip_address
}
