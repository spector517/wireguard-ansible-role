# "WireGuard" Ansible role

Deploy WireGuard VPN server and generate clients configs

## Requirements

Remotes:
- Based on Debian OS (Ubuntu 20.04+ is recommended)
- Root access
- Internet connection

Inventory file:
- localhost must be present

## Role required variables
```
### Required variables

# Your WireGuard VPN server URL
wireguard_url: your-vpn-server.com

# List of clients names
wireguard_clients:
  - client1
  - client2

# true if you want use the Uncomplicated Firewall
wireguard_use_ufw: false
```

## Role all variables
```
### Connection and network variables
# Your server url, port, network interface name and network address
wireguard_url: your-vpn-server.com
wireguard_port: 51820
wireguard_network_interface: wg0
wireguard_network_address: 10.9.0.1/24

# Method of apply server changes - restart or reload
wireguard_apply_changes_method: restart

# Wireguard apt package version
wireguard_package_version: latest

# List of clients names
wireguard_clients:
  - client1

# List of DNS-servers
wireguard_dns:
  - 1.1.1.1

# true if you want use the Uncomplicated Firewall
wireguard_use_ufw: false

# Path to directory containing server and clients configs (on storage server and localhost)
wireguard_storage_path: ~/wg-storage

# Server for directory containing server and clients configs
wireguard_storage_server: localhost
```

## Dependencies

- Ansible community module 'community.general.ufw' must be installed

## Example playbook

```
- hosts: all
  roles:
  - role: spector517.wireguard
```

## Example inventory

```
[you-wg-server]
your-server.com

[local]
localhost ansible_connection=local
```

## Usage server after installation

- Download the client app for your OS from [wireguard.com](https://www.wireguard.com/install/)
- Import the client config file in the client app
- Connect to WireGuard server using imported client config

# License

MIT
