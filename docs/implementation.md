# Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the office network design using Cisco Packet Tracer. Follow these procedures to build the complete network infrastructure.

## Prerequisites

### Software Requirements
- **Cisco Packet Tracer**: Version 7.0 or higher
- **Basic Networking Knowledge**: Understanding of VLANs, routing, switching
- **Time Allocation**: 2-3 hours for complete implementation

### Hardware Requirements
- **Computer**: Minimum 4GB RAM, 2GHz processor
- **Storage**: 2GB free disk space
- **Display**: 1024x768 resolution minimum

## Step 1: Project Setup

### Create New Project
1. Open Cisco Packet Tracer
2. Click **File → New**
3. Save project as `Office System Network Design.pkt`
4. Set workspace name to "Office Network Design"

### Configure Workspace
1. Set grid display for precise placement
2. Enable device labels
3. Configure interface names
4. Set background color for better visibility

## Step 2: Device Placement

### Core Layer Devices
1. **Router**: Add 1x Cisco 2911 router
   - Place at top center
   - Label: "Core-Router-01"
   
2. **Core Switch**: Add 1x Cisco 3560 switch
   - Place below router
   - Label: "Core-Switch-01"

### Distribution Layer Devices
1. **Distribution Switches**: Add 2x Cisco 3560 switches
   - Place below core switch
   - Labels: "Dist-Switch-01", "Dist-Switch-02"

### Access Layer Devices
1. **Access Switches**: Add 4x Cisco 2960 switches
   - Place below distribution switches
   - Labels: "Access-Switch-01" through "Access-Switch-04"

### Security Devices
1. **Firewall**: Add 1x ASA 5505 firewall
   - Place between router and internet cloud
   - Label: "ASA-Firewall-01"

### End Devices
1. **Servers**: Add 5x servers
   - Place near Access-Switch-03
   - Labels: "DC", "File-Server", "App-Server", "DB-Server", "Backup-Server"

2. **Workstations**: Add 10x PCs
   - Distribute among access switches
   - Labels: "PC-01" through "PC-10"

3. **IP Phones**: Add 5x IP phones
   - Connect to access switches
   - Labels: "Phone-01" through "Phone-05"

4. **Wireless APs**: Add 2x wireless access points
   - Connect to Access-Switch-02 and Access-Switch-04
   - Labels: "AP-01", "AP-02"

5. **Laptops**: Add 3x laptops for wireless testing
   - Place near access points

## Step 3: Physical Connections

### Core Layer Connections
1. **Internet Cloud → Firewall**: Copper Straight-Through
2. **Firewall → Core Router**: Copper Straight-Through
3. **Core Router → Core Switch**: Copper Straight-Through

### Distribution Layer Connections
1. **Core Switch → Dist-Switch-01**: Fiber Optic
2. **Core Switch → Dist-Switch-02**: Fiber Optic
3. **Dist-Switch-01 → Dist-Switch-02**: Fiber Optic (redundancy)

### Access Layer Connections
1. **Dist-Switch-01 → Access-Switch-01**: Copper Straight-Through
2. **Dist-Switch-01 → Access-Switch-02**: Copper Straight-Through
3. **Dist-Switch-02 → Access-Switch-03**: Copper Straight-Through
4. **Dist-Switch-02 → Access-Switch-04**: Copper Straight-Through

### End Device Connections
1. **Servers → Access-Switch-03**: Copper Straight-Through
2. **Workstations → Access Switches**: Copper Straight-Through
3. **IP Phones → Access Switches**: Copper Straight-Through
4. **Wireless APs → Access Switches**: Copper Straight-Through

## Step 4: VLAN Configuration

### Core Switch VLAN Configuration
```cli
enable
configure terminal
! Create VLANs
vlan 10
 name Management
vlan 20
 name Employees
vlan 30
 name Guests
vlan 40
 name Servers
vlan 50
 name DMZ
vlan 60
 name Voice
! Configure SVI interfaces
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface vlan 30
 ip address 192.168.30.1 255.255.255.0
 no shutdown
interface vlan 40
 ip address 192.168.40.1 255.255.255.0
 no shutdown
interface vlan 50
 ip address 192.168.50.1 255.255.255.0
 no shutdown
interface vlan 60
 ip address 192.168.60.1 255.255.255.0
 no shutdown
end
write memory
```

### Distribution Switch VLAN Configuration
```cli
enable
configure terminal
! Create same VLANs as core switch
vlan 10
 name Management
vlan 20
 name Employees
vlan 30
 name Guests
vlan 40
 name Servers
vlan 50
 name DMZ
vlan 60
 name Voice
! Configure trunk ports to core switch
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,60
 switchport trunk native vlan 99
 no shutdown
! Configure trunk ports to access switches
interface range GigabitEthernet0/2 - 3
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,60
 switchport trunk native vlan 99
 no shutdown
end
write memory
```

## Step 5: Access Switch Configuration

### Access Switch 1 Configuration (Employee Workstations)
```cli
enable
configure terminal
! Create VLANs
vlan 10
 name Management
vlan 20
 name Employees
! Configure uplink trunk
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 switchport trunk native vlan 99
 no shutdown
! Configure access ports for workstations
interface range FastEthernet0/2 - 10
 switchport mode access
 switchport access vlan 20
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 spanning-tree portfast
 no shutdown
! Configure management interface
interface vlan 10
 ip address 192.168.10.10 255.255.255.0
 no shutdown
ip default-gateway 192.168.10.1
end
write memory
```

### Access Switch 2 Configuration (Printers and Wireless)
```cli
enable
configure terminal
! Create VLANs
vlan 10
 name Management
vlan 20
 name Employees
vlan 30
 name Guests
! Configure uplink trunk
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99
 no shutdown
! Configure access ports for printers
interface range FastEthernet0/2 - 5
 switchport mode access
 switchport access vlan 20
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 spanning-tree portfast
 no shutdown
! Configure wireless AP port
interface FastEthernet0/6
 switchport mode trunk
 switchport trunk allowed vlan 20,30
 switchport trunk native vlan 99
 no shutdown
! Configure management interface
interface vlan 10
 ip address 192.168.10.11 255.255.255.0
 no shutdown
ip default-gateway 192.168.10.1
end
write memory
```

### Access Switch 3 Configuration (Servers)
```cli
enable
configure terminal
! Create VLANs
vlan 10
 name Management
vlan 40
 name Servers
! Configure uplink trunk
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,40
 switchport trunk native vlan 99
 no shutdown
! Configure access ports for servers
interface range FastEthernet0/2 - 10
 switchport mode access
 switchport access vlan 40
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 spanning-tree portfast
 no shutdown
! Configure management interface
interface vlan 10
 ip address 192.168.10.12 255.255.255.0
 no shutdown
ip default-gateway 192.168.10.1
end
write memory
```

### Access Switch 4 Configuration (Management and Voice)
```cli
enable
configure terminal
! Create VLANs
vlan 10
 name Management
vlan 60
 name Voice
! Configure uplink trunk
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,60
 switchport trunk native vlan 99
 no shutdown
! Configure access ports for IP phones
interface range FastEthernet0/2 - 6
 switchport mode access
 switchport access vlan 60
 switchport voice vlan 60
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 spanning-tree portfast
 no shutdown
! Configure management interface
interface vlan 10
 ip address 192.168.10.13 255.255.255.0
 no shutdown
ip default-gateway 192.168.10.1
end
write memory
```

## Step 6: Router Configuration

### Core Router Configuration
```cli
enable
configure terminal
! Configure hostname
hostname Core-Router-01
! Configure WAN interface
interface GigabitEthernet0/0
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
 no shutdown
! Configure LAN interface
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 ip nat inside
 no shutdown
! Configure subinterfaces for VLANs
interface GigabitEthernet0/1.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 ip nat inside
interface GigabitEthernet0/1.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 ip nat inside
interface GigabitEthernet0/1.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 ip nat inside
interface GigabitEthernet0/1.40
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
 ip nat inside
interface GigabitEthernet0/1.50
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.0
 ip nat inside
interface GigabitEthernet0/1.60
 encapsulation dot1Q 60
 ip address 192.168.60.1 255.255.255.0
 ip nat inside
! Configure routing
ip routing
! Configure default route
ip route 0.0.0.0 0.0.0.0 203.0.113.1
! Configure OSPF
router ospf 1
 router-id 192.168.1.1
 network 192.168.0.0 0.0.255.255 area 0
! Configure NAT
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface GigabitEthernet0/0 overload
! Configure static NAT for servers
ip nat inside source static 192.168.50.10 203.0.113.10
ip nat inside source static 192.168.50.20 203.0.113.20
ip nat inside source static 192.168.50.30 203.0.113.30
end
write memory
```

## Step 7: DHCP Configuration

### Router DHCP Configuration
```cli
enable
configure terminal
! Configure DHCP pool for employees
ip dhcp pool EMPLOYEES
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 8.8.8.8 8.8.4.4
 domain-name office.local
 lease 0 8
! Configure DHCP pool for guests
ip dhcp pool GUESTS
 network 192.168.30.0 255.255.255.0
 default-router 192.168.30.1
 dns-server 8.8.8.8 8.8.4.4
 domain-name guest.office.local
 lease 0 2
! Configure DHCP pool for voice
ip dhcp pool VOICE
 network 192.168.60.0 255.255.255.0
 default-router 192.168.60.1
 dns-server 8.8.8.8 8.8.4.4
 domain-name voice.office.local
 lease 1
 option 150 ip 192.168.60.10
! Exclude addresses from DHCP pools
ip dhcp excluded-address 192.168.20.1 192.168.20.49
ip dhcp excluded-address 192.168.30.1 192.168.30.49
ip dhcp excluded-address 192.168.60.1 192.168.60.49
end
write memory
```

## Step 8: Wireless Configuration

### Access Point Configuration
```cli
enable
configure terminal
! Configure corporate SSID
dot11 ssid Corporate
 vlan 20
 authentication open eap eap_methods
 authentication key-management wpa version 2
 wpa-psk ascii 7 YourSecurePasswordHere
! Configure guest SSID
dot11 ssid Guest
 vlan 30
 authentication open
 guest-mode
! Configure radio interfaces
interface Dot11Radio0
 ssid Corporate
 encryption mode ciphers aes-ccm
 channel 6
 speed basic-5.5 6.0 9.0 11.0 12.0 18.0 24.0 36.0 48.0 54.0
 no shutdown
interface Dot11Radio1
 ssid Guest
 encryption mode ciphers aes-ccm
 channel 11
 speed basic-5.5 6.0 9.0 11.0 12.0 18.0 24.0 36.0 48.0 54.0
 no shutdown
! Configure bridge interface
interface BVI1
 ip address 192.168.20.254 255.255.255.0
 no shutdown
end
write memory
```

## Step 9: Server Configuration

### Domain Controller Configuration
1. **Static IP**: 192.168.40.10/24
2. **Gateway**: 192.168.40.1
3. **DNS**: 192.168.40.10 (primary), 8.8.8.8 (secondary)
4. **Domain**: office.local
5. **Roles**: Active Directory, DNS, DHCP (optional)

### File Server Configuration
1. **Static IP**: 192.168.40.20/24
2. **Gateway**: 192.168.40.1
3. **DNS**: 192.168.40.10, 8.8.8.8
4. **Shares**: Department folders, user home directories
5. **Permissions**: NTFS permissions configured

### Web Server Configuration
1. **Static IP**: 192.168.50.10/24
2. **Gateway**: 192.168.50.1
3. **DNS**: 8.8.8.8, 8.8.4.4
4. **Services**: HTTP, HTTPS
5. **Firewall**: Windows Firewall configured

## Step 10: Testing and Verification

### Connectivity Testing
1. **Ping Tests**:
   - From employee PC to gateway
   - From employee PC to server
   - From guest PC to internet
   - From server to internet

2. **Traceroute Tests**:
   - Verify path to internet
   - Verify inter-VLAN routing
   - Verify failover paths

3. **Application Testing**:
   - Web browsing
   - Email access
   - File sharing
   - VoIP calls

### Security Testing
1. **ACL Verification**:
   - Test guest isolation
   - Test server access restrictions
   - Test management access

2. **Port Security**:
   - Test MAC address limits
   - Test violation actions
   - Test sticky MAC learning

3. **Wireless Security**:
   - Test authentication
   - Test encryption
   - Test guest isolation

## Step 11: Documentation

### Configuration Backup
1. **Save Running Config**:
   ```cli
   copy running-config startup-config
   ```

2. **Export Configurations**:
   - Save to text files
   - Version control with Git
   - Document changes

### Network Diagram
1. **Create Topology Diagram**:
   - Use Packet Tracer export
   - Add IP addressing information
   - Include VLAN details

2. **Documentation Files**:
   - IP addressing scheme
   - Security policies
   - Implementation procedures

## Troubleshooting Guide

### Common Issues

#### VLAN Problems
- **Symptom**: Cannot communicate between VLANs
- **Solution**: Check trunk configuration, verify VLAN database
- **Commands**: `show vlan brief`, `show interfaces trunk`

#### DHCP Issues
- **Symptom**: Devices not getting IP addresses
- **Solution**: Check DHCP pool configuration, verify excluded addresses
- **Commands**: `show ip dhcp binding`, `show ip dhcp pool`

#### Routing Problems
- **Symptom**: Cannot reach remote networks
- **Solution**: Check routing table, verify OSPF adjacency
- **Commands**: `show ip route`, `show ip ospf neighbor`

#### Security Issues
- **Symptom**: Access denied to resources
- **Solution**: Check ACL configuration, verify NAT rules
- **Commands**: `show access-lists`, `show ip nat translations`

### Debug Commands
```cli
! Debug VLAN issues
debug vlan events

! Debug routing issues
debug ip ospf events
debug ip routing

! Debug DHCP issues
debug ip dhcp server events

! Debug security issues
debug ip packet
```

## Final Verification Checklist

- [ ] All devices powered on and connected
- [ ] VLANs created and configured
- [ ] Trunk links operational
- [ ] IP addressing configured correctly
- [ ] Routing protocols operational
- [ ] DHCP pools working
- [ ] Internet connectivity functional
- [ ] Security policies enforced
- [ ] Wireless networks operational
- [ ] Documentation complete
- [ ] Backups created
- [ ] Testing completed successfully

## Next Steps

After successful implementation:

1. **Monitor Performance**: Use SNMP and logging
2. **Regular Maintenance**: Schedule updates and backups
3. **Security Audits**: Regular vulnerability assessments
4. **Capacity Planning**: Monitor growth and plan expansion
5. **User Training**: Educate users on network policies

This completes the implementation of your office network design. The network is now ready for production use with enterprise-level security and performance.
