# Security Policy

## Overview

This document outlines the comprehensive security policy implemented for the office network design, ensuring protection against unauthorized access, data breaches, and network threats.

## Security Architecture

### Defense in Depth Strategy

The network implements a multi-layered security approach:

1. **Perimeter Security**: Firewall and border protection
2. **Network Security**: Segmentation and access control
3. **Host Security**: Endpoint protection
4. **Application Security**: Application-level filtering
5. **Data Security**: Encryption and data protection

## Firewall Configuration

### Cisco ASA Firewall Rules

#### Inbound Rules (WAN to DMZ)
| Source | Destination | Port | Protocol | Action | Description |
|--------|-------------|------|----------|--------|-------------|
| Any | 203.0.113.10 | 80,443 | TCP | Allow | Web server access |
| Any | 203.0.113.20 | 25,587,993,995 | TCP | Allow | Email services |
| Any | 203.0.113.30 | 443 | TCP | Allow | VPN access |
| Any | Any | Any | Any | Deny | Default deny |

#### Outbound Rules (Internal to WAN)
| Source | Destination | Port | Protocol | Action | Description |
|--------|-------------|------|----------|--------|-------------|
| 192.168.20.0/24 | Any | 80,443 | TCP | Allow | Employee web access |
| 192.168.30.0/24 | Any | 80,443 | TCP | Allow | Guest web access |
| 192.168.40.0/24 | Any | 80,443,53 | TCP/UDP | Allow | Server updates |
| Any | Any | Any | Any | Deny | Default deny |

#### Internal Rules (VLAN to VLAN)
| Source VLAN | Destination VLAN | Port | Protocol | Action | Description |
|-------------|------------------|------|----------|--------|-------------|
| 20 (Employees) | 40 (Servers) | 53,88,389,636 | TCP/UDP | Allow | Domain services |
| 20 (Employees) | 40 (Servers) | 80,443,445 | TCP | Allow | Application access |
| 30 (Guests) | 10,20,40,50 | Any | Any | Deny | Guest isolation |
| 10 (Management) | Any | 22,23,443 | TCP | Allow | Management access |

## Access Control Lists (ACLs)

### Standard ACLs
```
! Management ACL
access-list 10 permit 192.168.10.0 0.0.0.255
access-list 10 deny any

! Server ACL
access-list 20 permit 192.168.40.0 0.0.0.255
access-list 20 deny any
```

### Extended ACLs
```
! Employee to Server ACL
access-list 101 permit tcp 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255 eq 80
access-list 101 permit tcp 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255 eq 443
access-list 101 permit tcp 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255 eq 445
access-list 101 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255
access-list 101 permit ip any any

! Guest Network ACL
access-list 102 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
access-list 102 deny ip 192.168.30.0 0.0.0.255 192.168.20.0 0.0.0.255
access-list 102 deny ip 192.168.30.0 0.0.0.255 192.168.40.0 0.0.0.255
access-list 102 deny ip 192.168.30.0 0.0.0.255 192.168.50.0 0.0.0.255
access-list 102 permit tcp 192.168.30.0 0.0.0.255 any eq 80
access-list 102 permit tcp 192.168.30.0 0.0.0.255 any eq 443
access-list 102 permit udp 192.168.30.0 0.0.0.255 any eq 53
access-list 102 deny ip any any
```

## Port Security

### Switch Port Security Configuration
```
! Enable port security globally
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security violation shutdown
switchport port-security aging time 5
switchport port-security aging type inactivity
```

### MAC Address Filtering
- **Static MAC Addresses**: Network infrastructure devices
- **Sticky MAC**: Dynamic learning with persistence
- **Maximum MAC Addresses**: 2 per port (device + IP phone)
- **Violation Mode**: Shutdown port on violation

## VLAN Security

### VLAN Access Control
- **Private VLANs**: Isolate ports within same VLAN
- **VLAN ACLs**: Apply filters at VLAN level
- **VLAN Hopping Prevention**: Disable unused ports
- **Native VLAN**: Use VLAN 99 for security

### Trunk Security
```
! Trunk port security
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,40,50,60
switchport nonegotiate
spanning-tree portfast trunk
```

## Wireless Security

### Wireless Authentication
- **Corporate SSID**: WPA2-Enterprise with RADIUS
- **Guest SSID**: Captive portal authentication
- **Management SSID**: WPA2-Personal with strong passwords

### WPA2-Enterprise Configuration
- **Authentication Server**: RADIUS server at 192.168.40.10
- **Encryption**: AES-CCMP
- **Key Management**: 802.1X/EAP-TLS
- **Certificate Authority**: Internal CA

### Guest Network Security
- **Captive Portal**: Web-based authentication
- **Session Timeout**: 2 hours
- **Bandwidth Limiting**: 1 Mbps per user
- **Content Filtering**: Block inappropriate content

## VPN Security

### Remote Access VPN
- **Protocol**: IPsec/IKEv2
- **Authentication**: Two-factor authentication
- **Encryption**: AES-256
- **Integrity**: SHA-256

### VPN Configuration
```
! IPsec VPN Configuration
crypto ipsec transform-set ESP-AES256-SHA256 esp-aes-256 esp-sha256-hmac
crypto ipsec security-association lifetime seconds 3600
crypto map VPN-MAP 10 ipsec-isakmp
crypto map VPN-MAP 10 match address VPN-ACL
crypto map VPN-MAP 10 set transform-set ESP-AES256-SHA256
crypto map VPN-MAP 10 set peer 203.0.113.30
```

## Intrusion Detection and Prevention

### IDS/IPS Configuration
- **Network IDS**: Snort or similar
- **Host-based IDS**: OSSEC on critical servers
- **Signature Updates**: Daily updates
- **Alerting**: Email and SMS notifications

### Monitoring Rules
- **Port Scanning**: Detect and block
- **Brute Force**: Detect multiple failed attempts
- **Malware Traffic**: Block known malicious IPs
- **Data Exfiltration**: Monitor large data transfers

## Logging and Monitoring

### Syslog Configuration
```
! Syslog Server Configuration
logging host 192.168.10.100
logging trap informational
logging facility local7
logging source-interface Loopback0
```

### SNMP Monitoring
- **SNMP Version**: v3 with encryption
- **Community Strings**: Complex and unique
- **Trap Receivers**: Network management system
- **Monitoring**: CPU, memory, interface status

### Event Correlation
- **SIEM Integration**: Centralized log analysis
- **Real-time Alerts**: Critical security events
- **Trending Analysis**: Baseline establishment
- **Compliance Reporting**: Automated reports

## Patch Management

### Network Device Updates
- **Firmware Updates**: Quarterly schedule
- **Security Patches**: Immediate deployment
- **Backup Configurations**: Before updates
- **Rollback Plan**: Update failure recovery

### Server Patching
- **Windows Updates**: WSUS management
- **Linux Updates**: Automated with Ansible
- **Application Updates**: Vendor coordination
- **Testing**: Pre-deployment validation

## Backup and Recovery

### Configuration Backups
- **Daily Backups**: Automated configuration backup
- **Off-site Storage**: Secure cloud storage
- **Version Control**: Git repository for configs
- **Recovery Testing**: Monthly restoration tests

### Disaster Recovery
- **RTO**: 4 hours for critical systems
- **RPO**: 1 hour maximum data loss
- **Alternate Site**: Cloud-based recovery
- **Documentation**: Detailed recovery procedures

## Compliance Requirements

### Industry Standards
- **ISO 27001**: Information security management
- **PCI DSS**: Payment card industry (if applicable)
- **HIPAA**: Healthcare information (if applicable)
- **GDPR**: Data protection (if applicable)

### Audit Trail
- **User Activity**: Complete logging
- **Configuration Changes**: Detailed audit log
- **Access Attempts**: Failed and successful
- **Data Access**: File and database access

## Security Policies

### Acceptable Use Policy
- **Personal Use**: Limited during business hours
- **Software Installation**: IT approval required
- **Data Classification**: Confidential, internal, public
- **Remote Access**: Company devices only

### Password Policy
- **Complexity**: Minimum 12 characters
- **Rotation**: Every 90 days
- **History**: Last 12 passwords remembered
- **Lockout**: 5 failed attempts, 30-minute lockout

### Incident Response Plan
1. **Detection**: Identify security incident
2. **Containment**: Isolate affected systems
3. **Eradication**: Remove threat
4. **Recovery**: Restore normal operations
5. **Lessons Learned**: Post-incident analysis

## Security Training

### Employee Training
- **Security Awareness**: Quarterly training
- **Phishing Simulation**: Monthly tests
- **Best Practices**: Ongoing education
- **Reporting**: Incident reporting procedures

### Technical Training
- **Network Security**: Advanced training for IT staff
- **Certification**: CISSP, CompTIA Security+
- **Workshops**: Hands-on security labs
- **Conferences**: Industry security events

## Review and Update

### Policy Review
- **Annual Review**: Complete policy assessment
- **Technology Changes**: Update as needed
- **Threat Landscape**: Adapt to new threats
- **Regulatory Changes**: Compliance updates

### Continuous Improvement
- **Security Metrics**: KPI tracking
- **Penetration Testing**: Annual security assessment
- **Vulnerability Scanning**: Monthly automated scans
- **Risk Assessment**: Quarterly evaluation
