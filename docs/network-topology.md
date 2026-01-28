# Network Topology

## Overview

This document describes the complete network topology for the office network design implemented in Cisco Packet Tracer.

## Network Architecture

### Hierarchical Design Model

The network follows the Cisco hierarchical design model with three distinct layers:

#### 1. Core Layer
- **Purpose**: High-speed switching and routing backbone
- **Components**: 
  - Core Switch (Layer 3)
  - Core Router
- **Features**:
  - Redundant paths
  - High availability
  - Fast convergence

#### 2. Distribution Layer
- **Purpose**: Routing between VLANs, policy implementation
- **Components**:
  - Distribution Switches (Layer 3)
  - Router-on-a-stick configuration
- **Features**:
  - Inter-VLAN routing
  - Access control lists
  - Quality of Service (QoS)

#### 3. Access Layer
- **Purpose**: End-device connectivity
- **Components**:
  - Access Switches (Layer 2)
  - Wireless Access Points
- **Features**:
  - Port security
  - VLAN assignment
  - Power over Ethernet (PoE)

## Physical Topology

### Main Components

| Device Type | Model | Quantity | Purpose |
|-------------|-------|----------|---------|
| Core Router | Cisco 2911 | 1 | Internet connectivity, routing |
| Core Switch | Cisco 3560 | 1 | Backbone switching |
| Distribution Switch | Cisco 3560 | 2 | Inter-VLAN routing |
| Access Switch | Cisco 2960 | 4 | End-device connectivity |
| Wireless AP | Cisco Aironet | 2 | Wireless access |
| Firewall | ASA 5505 | 1 | Security filtering |

### Connection Layout

```
Internet
    |
[Firewall]
    |
[Core Router]
    |
[Core Switch]
    |
    ├── [Distribution Switch 1] ──── [Access Switch 1] ──── Workstations
    │                                   ├── [Access Switch 2] ──── Printers
    │                                   └── [Wireless AP 1]
    │
    └── [Distribution Switch 2] ──── [Access Switch 3] ──── Servers
                                    ├── [Access Switch 4] ──── Management
                                    └── [Wireless AP 2]
```

## Logical Topology

### VLAN Design

| VLAN ID | Name | Purpose | IP Subnet | Gateway |
|---------|------|---------|-----------|---------|
| 10 | Management | Network management | 192.168.10.0/24 | 192.168.10.1 |
| 20 | Employees | Staff workstations | 192.168.20.0/24 | 192.168.20.1 |
| 30 | Guests | Guest wireless | 192.168.30.0/24 | 192.168.30.1 |
| 40 | Servers | Internal servers | 192.168.40.0/24 | 192.168.40.1 |
| 50 | DMZ | Public servers | 192.168.50.0/24 | 192.168.50.1 |

### Trunk Configuration

- **Core to Distribution**: 802.1Q trunk carrying all VLANs
- **Distribution to Access**: 802.1Q trunk with specific VLAN pruning
- **Native VLAN**: VLAN 99 (unused for security)

## Redundancy Design

### High Availability Features
- **HSRP**: Hot Standby Router Protocol for gateway redundancy
- **STP**: Spanning Tree Protocol for loop prevention
- **Link Aggregation**: EtherChannel for increased bandwidth
- **Redundant Power**: Dual power supplies on core devices

### Failover Mechanisms
- **Primary/Secondary**: HSRP priority configuration
- **Fast Convergence**: OSPF routing protocol
- **Automatic Failover**: STP rapid convergence

## Security Zones

### Network Segmentation
- **Trusted Zone**: Internal network (VLANs 10, 20, 40)
- **Untrusted Zone**: Guest network (VLAN 30)
- **DMZ Zone**: Public-facing servers (VLAN 50)
- **Management Zone**: Network infrastructure (VLAN 10)

### Access Control
- **ACLs**: Applied at distribution layer
- **Firewall Rules**: Stateful inspection at edge
- **Port Security**: MAC address filtering
- **VLAN Access Control**: Layer 2 security policies

## Wireless Design

### Wireless Network Segments
- **Corporate SSID**: VLAN 20 (WPA2-Enterprise)
- **Guest SSID**: VLAN 30 (Captive Portal)
- **Management SSID**: VLAN 10 (WPA2-Personal)

### Wireless Security
- **WPA2-Enterprise**: RADIUS authentication
- **Captive Portal**: Guest authentication
- **MAC Filtering**: Additional security layer
- **Wireless IDS**: Intrusion detection system

## IP Telephony Integration

### VoIP Requirements
- **QoS**: Priority queuing for voice traffic
- **Power over Ethernet**: PoE switches for IP phones
- **VLAN Separation**: Voice VLAN (VLAN 60)
- **Call Manager**: IP PBX integration

### Voice Quality Features
- **Traffic Shaping**: Bandwidth allocation
- **Latency Optimization**: < 150ms delay
- **Jitter Control**: Buffer management
- **Echo Cancellation**: Voice enhancement

## Monitoring and Management

### Network Management
- **SNMP**: Simple Network Management Protocol
- **Syslog**: Centralized logging
- **NetFlow**: Traffic analysis
- **NMS**: Network Management System

### Performance Monitoring
- **Bandwidth Utilization**: Real-time monitoring
- **Device Health**: CPU, memory, temperature
- **Link Status**: Interface monitoring
- **Error Rates**: Packet loss analysis
