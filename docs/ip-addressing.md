# IP Addressing Scheme

## Overview

This document outlines the comprehensive IP addressing scheme for the office network design, ensuring efficient utilization of address space and proper network segmentation.

## Address Space Allocation

### Private IP Address Ranges
- **Primary Network**: 192.168.0.0/16 (Class B private)
- **Management**: 192.168.10.0/24
- **Employee Network**: 192.168.20.0/24
- **Guest Network**: 192.168.30.0/24
- **Server Network**: 192.168.40.0/24
- **DMZ Network**: 192.168.50.0/24
- **Voice Network**: 192.168.60.0/24

## VLAN IP Addressing

### VLAN 10 - Management Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| Core Switch | 192.168.10.1 | 255.255.255.0 | N/A | Management interface |
| Distribution Switch 1 | 192.168.10.2 | 255.255.255.0 | 192.168.10.1 | Management |
| Distribution Switch 2 | 192.168.10.3 | 255.255.255.0 | 192.168.10.1 | Management |
| Access Switch 1 | 192.168.10.10 | 255.255.255.0 | 192.168.10.1 | Management |
| Access Switch 2 | 192.168.10.11 | 255.255.255.0 | 192.168.10.1 | Management |
| Access Switch 3 | 192.168.10.12 | 255.255.255.0 | 192.168.10.1 | Management |
| Access Switch 4 | 192.168.10.13 | 255.255.255.0 | 192.168.10.1 | Management |
| Network Monitor | 192.168.10.100 | 255.255.255.0 | 192.168.10.1 | NMS Server |

### VLAN 20 - Employee Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| SVI Interface | 192.168.20.1 | 255.255.255.0 | N/A | Default gateway |
| DHCP Server | 192.168.20.5 | 255.255.255.0 | 192.168.20.1 | IP allocation |
| Employee Workstations | 192.168.20.50-200 | 255.255.255.0 | 192.168.20.1 | End devices |
| Network Printers | 192.168.20.10-19 | 255.255.255.0 | 192.168.20.1 | Print services |

### VLAN 30 - Guest Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| SVI Interface | 192.168.30.1 | 255.255.255.0 | N/A | Default gateway |
| DHCP Server | 192.168.30.5 | 255.255.255.0 | 192.168.30.1 | Guest IP allocation |
| Guest Devices | 192.168.30.50-200 | 255.255.255.0 | 192.168.30.1 | Temporary access |

### VLAN 40 - Server Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| SVI Interface | 192.168.40.1 | 255.255.255.0 | N/A | Default gateway |
| Domain Controller | 192.168.40.10 | 255.255.255.0 | 192.168.40.1 | Active Directory |
| File Server | 192.168.40.20 | 255.255.255.0 | 192.168.40.1 | File storage |
| Application Server | 192.168.40.30 | 255.255.255.0 | 192.168.40.1 | Business apps |
| Database Server | 192.168.40.40 | 255.255.255.0 | 192.168.40.1 | Database services |
| Backup Server | 192.168.40.50 | 255.255.255.0 | 192.168.40.1 | Backup storage |

### VLAN 50 - DMZ Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| SVI Interface | 192.168.50.1 | 255.255.255.0 | N/A | Default gateway |
| Web Server | 192.168.50.10 | 255.255.255.0 | 192.168.50.1 | Public web services |
| Mail Server | 192.168.50.20 | 255.255.255.0 | 192.168.50.1 | Email services |
| VPN Server | 192.168.50.30 | 255.255.255.0 | 192.168.50.1 | Remote access |

### VLAN 60 - Voice Network
| Device | IP Address | Subnet Mask | Gateway | Purpose |
|--------|------------|-------------|---------|---------|
| SVI Interface | 192.168.60.1 | 255.255.255.0 | N/A | Default gateway |
| Call Manager | 192.168.60.10 | 255.255.255.0 | 192.168.60.1 | IP PBX |
| IP Phones | 192.168.60.50-150 | 255.255.255.0 | 192.168.60.1 | VoIP endpoints |
| Voice Gateway | 192.168.60.5 | 255.255.255.0 | 192.168.60.1 | PSTN connectivity |

## Router Interfaces

### Core Router
| Interface | IP Address | Subnet Mask | Purpose |
|-----------|------------|-------------|---------|
| Gig0/0 (WAN) | 203.0.113.2 | 255.255.255.252 | Internet connection |
| Gig0/1 (LAN) | 192.168.1.1 | 255.255.255.0 | Internal network |

### Distribution Router (if applicable)
| Interface | IP Address | Subnet Mask | Purpose |
|-----------|------------|-------------|---------|
| Gig0/0 | 192.168.1.2 | 255.255.255.0 | Core connectivity |
| Gig0/1.10 | 192.168.10.1 | 255.255.255.0 | VLAN 10 gateway |
| Gig0/1.20 | 192.168.20.1 | 255.255.255.0 | VLAN 20 gateway |
| Gig0/1.30 | 192.168.30.1 | 255.255.255.0 | VLAN 30 gateway |
| Gig0/1.40 | 192.168.40.1 | 255.255.255.0 | VLAN 40 gateway |
| Gig0/1.50 | 192.168.50.1 | 255.255.255.0 | VLAN 50 gateway |

## DHCP Configuration

### DHCP Scopes
| Network | Pool Range | Excluded Range | Lease Duration |
|---------|------------|---------------|----------------|
| 192.168.20.0/24 | 192.168.20.50-200 | 192.168.20.1-49 | 8 hours |
| 192.168.30.0/24 | 192.168.30.50-200 | 192.168.30.1-49 | 2 hours |
| 192.168.60.0/24 | 192.168.60.50-150 | 192.168.60.1-49 | 24 hours |

### DHCP Options
- **Option 3**: Default Gateway
- **Option 6**: DNS Servers (8.8.8.8, 8.8.4.4)
- **Option 15**: Domain Name (office.local)
- **Option 51**: Lease Time
- **Option 150**: TFTP Server (for IP phones)

## DNS Configuration

### Internal DNS
- **Primary DNS**: 192.168.40.10 (Domain Controller)
- **Secondary DNS**: 192.168.40.20 (File Server)
- **Forwarders**: 8.8.8.8, 8.8.4.4 (Google DNS)

### DNS Records
- **A Records**: All servers and network devices
- **CNAME Records**: Service aliases
- **MX Records**: Mail server configuration
- **SRV Records**: Service discovery

## NAT Configuration

### Static NAT
| Internal IP | Public IP | Service |
|-------------|-----------|---------|
| 192.168.50.10 | 203.0.113.10 | Web Server |
| 192.168.50.20 | 203.0.113.20 | Mail Server |
| 192.168.50.30 | 203.0.113.30 | VPN Server |

### Dynamic NAT (PAT)
- **Internal Network**: 192.168.20.0/24, 192.168.30.0/24
- **Public IP Pool**: 203.0.113.100-110
- **Overload**: Enabled

## Routing Protocols

### OSPF Configuration
- **Process ID**: 1
- **Router ID**: 192.168.1.1
- **Area**: 0.0.0.0 (Backbone area)
- **Network Statements**: All internal networks
- **Cost Calculation**: Based on bandwidth

### Static Routes
- **Default Route**: 0.0.0.0/0 via 203.0.113.1 (ISP)
- **Summary Routes**: For external networks

## IP Address Management

### Address Allocation Strategy
- **Sequential Assignment**: For network devices
- **Random Assignment**: For end devices (DHCP)
- **Reserved Addresses**: For servers and infrastructure
- **Future Growth**: 20% address space reserved

### Documentation
- **IP Address Spreadsheet**: Complete inventory
- **Network Diagrams**: Visual representation
- **Configuration Files**: Device-specific settings
- **Change Management**: Tracking system

## Security Considerations

### IP Security
- **Anti-Spoofing**: ACLs to prevent IP spoofing
- **Private Addresses**: RFC 1918 compliance
- **NAT Isolation**: Internal network protection
- **Firewall Rules**: Traffic filtering

### Access Control
- **VLAN Isolation**: Layer 2 segmentation
- **ACL Placement**: Distribution layer filtering
- **DMZ Isolation**: Restricted access
- **Guest Network**: Limited connectivity

## Future Expansion

### Scalability Planning
- **Additional VLANs**: Up to VLAN 100
- **Subnet Expansion**: Larger address blocks
- **IPv6 Transition**: Dual-stack capability
- **Cloud Integration**: Hybrid connectivity

### Growth Scenarios
- **New Departments**: Additional VLANs
- **Remote Offices**: VPN connectivity
- **Wireless Expansion**: More access points
- **IoT Devices**: Dedicated network segment
