# Meadowbrook Medical — Multi-VLAN Network Design

A small clinic network built in Cisco Packet Tracer, designed from real business requirements. Demonstrates VLSM subnetting, VLANs, inter-VLAN routing (router-on-a-stick), and access control using ACLs.

## The brief

A small medical clinic, Meadowbrook Medical, needed a network that could:

- Separate reception/admin staff, clinical staff, and guest WiFi into isolated networks
- Give all three groups internet access via the clinic's ISP connection
- Allow reception to reach a shared printer in the clinical network
- Prevent clinical staff and guest WiFi from communicating with each other

The whole build was allocated the address block `192.168.50.0/24`.

## Network design

### Subnets (VLSM)

I split the /24 into three variably-sized subnets, biggest first:

| Group | VLAN | Subnet | Mask | Usable range | Broadcast | Gateway |
|---|---|---|---|---|---|---|
| Guest WiFi | 30 | 192.168.50.0/25 | 255.255.255.128 | .1 – .126 | .127 | 192.168.50.1 |
| Clinical | 20 | 192.168.50.128/26 | 255.255.255.192 | .129 – .190 | .191 | 192.168.50.129 |
| Reception | 10 | 192.168.50.192/26 | 255.255.255.192 | .193 – .254 | .255 | 192.168.50.193 |

Guest gets the biggest slice because guest traffic is the most variable — customers come and go all day. Reception and clinical are more predictable.

### Topology

- **Switch 1**: Reception (VLAN 10) and Clinical (VLAN 20) — 4 PCs
- **Switch 2**: Guest WiFi (VLAN 30) — 2 PCs
- **Router**: Two trunk links, one to each switch, using router-on-a-stick with subinterfaces per VLAN

Guest lives on its own switch on purpose — physical separation from clinical systems is a nice bonus on top of the logical VLAN boundary.

![Topology](topology.png)

## Key configuration

### Router (router-on-a-stick)

Physical interface has no IP — subinterfaces do all the work.

```
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.50.193 255.255.255.192

interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.50.129 255.255.255.192

interface GigabitEthernet0/1.30
 encapsulation dot1Q 30
 ip address 192.168.50.1 255.255.255.128
```

### Switches

Access ports assigned to their VLAN, uplink to router set as trunk.

```
vlan 10
 name ADMIN
vlan 20
 name CLINICAL

interface range FastEthernet0/1-2
 switchport mode access
 switchport access vlan 10

interface GigabitEthernet0/1
 switchport mode trunk
```

### Access control (ACL)

Extended ACLs applied inbound on the Guest and Clinical subinterfaces to block traffic between the two VLANs while allowing everything else.

```
access-list 100 deny ip 192.168.50.0 0.0.0.127 192.168.50.128 0.0.0.63
access-list 100 permit ip any any

interface GigabitEthernet0/1.30
 ip access-group 100 in
```

Same pattern applied on the Clinical subinterface for the reverse direction.

## Verification

- Devices in the same VLAN can ping each other
- Devices in different VLANs (allowed pairs) can route through the router
- Guest cannot reach Clinical (blocked by ACL) — router replies with "Destination host unreachable"
- Guest can still reach Reception and the internet gateway

Screenshots in `/screenshots/`.

## What I learnt

- **Subnet design comes before VLAN design** — each VLAN needs its own subnet, so the address plan has to account for how many VLANs you'll have from day one
- **Trunks are the most common failure point** — forgetting to trunk the switchport facing the router is why devices end up with 169.254.x.x addresses
- **ACLs enforce policy, but VLANs create the boundary** — VLANs alone don't secure anything without a policy layer on top
- **169.254 is a diagnostic signal** — it always means DHCP failed, which points to VLAN or trunk misconfiguration
- **The `switchport trunk allowed vlan` command replaces rather than adds** — one wrong command can knock out an entire network

## Files in this repo

- `meadowbrook.pkt` — Packet Tracer file
- `configs/` — running-config from each device
- `screenshots/` — verification screenshots
- `topology.png` — network diagram

## Skills demonstrated

Networking fundamentals · VLSM subnetting · VLAN configuration · 802.1Q trunking · Inter-VLAN routing (router-on-a-stick) · Cisco IOS CLI · Access Control Lists · Network design from business requirements · Troubleshooting
