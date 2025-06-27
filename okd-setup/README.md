# OKD on Proxmox Setup

This directory contains scripts and instructions for deploying an OKD 4.x cluster on Proxmox using Fedora CoreOS, based on the `pvelati/okd-proxmox-scripts` reference.

## Requirements

*   Proxmox 6.x
*   Sufficient resources (CPU, RAM, Disk as per OKD documentation)
*   DHCP reservation for nodes
*   DNS entries for nodes and HAProxy

## Installation Steps

1.  **Setup HAProxy:**
    Edit `setup-haproxy.sh` to configure IP addresses, then execute it:
    `sh setup-haproxy.sh`

2.  **Install Clients:**
    Run the client installation script:
    `sh setup-clients.sh`

3.  **Download and Extract QCOW2 Image:**
    Execute the script to download and prepare the QCOW2 image:
    `sh setup-qcow2-image.sh`

4.  **Create Template on Proxmox:**
    Run the script to create the Proxmox VM template:
    `sh setup-template.sh`

5.  **Compile `install-config`:**
    Refer to `compile-install-config.sh` for instructions on how to prepare your `install-config.yaml.ORe`.

## Management Scripts

*   **Clean:**
    `sh clean.sh` - Deletes all ignition files.

*   **Destroy:**
    `sh delete-all.sh` - Stops and deletes all VMs and the HAProxy LXC.
