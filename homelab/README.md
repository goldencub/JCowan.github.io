# Home Lab — Virtualised Network & Security Environment

> A VirtualBox home lab covering firewalls, subnetting, and network monitoring — built from scratch, documented as it breaks.

This lab is a hands-on environment for practising real networking and security skills outside the classroom. Every session is documented, including what went wrong and how it was diagnosed.

---

## Lab Architecture

| Component | Role |
|---|---|
| **Host Machine** | Windows 11, running VirtualBox |
| **pfSense VM** | Firewall and router between the internal lab and the host network |
| **Ubuntu VM** | Internal client machine — primary lab workstation |
| **Kali Linux VM** | Offensive security and pen-testing *(planned)* |
| **Windows Server VM** | Target machine for security testing *(planned)* |

All internal VMs sit behind pfSense on an isolated virtual network. pfSense acts as the gateway — the same role a physical firewall plays in a real network. Traffic from the internal VMs must pass through pfSense to reach the outside world.

---

## Sessions

Sessions are added as they're completed. All notes include what broke and what didn't work — not just the wins.

### ✅ Session 1 — Ubuntu VM Setup
**Date:** 20/07/2026

Installed Ubuntu Server on VirtualBox and confirmed internet connectivity. Noticed the VM received a `10.0.2.15` address rather than a `192.168.x.x` address, and diagnosed this as VirtualBox NAT mode creating its own private network inside the host.

**Key takeaway:** documented the NAT traffic flow —
`VM → VirtualBox router → host machine's real IP → internet`

[View session notes →]()

---

### ✅ Session 2 — GitHub Repository & Network Diagram
**Date:** 23/07/2026

Set up the GitHub portfolio repository and documented Session 1's findings. Designed the target lab architecture as a network diagram showing the relationships between host, hypervisor, pfSense, and the internal VMs.

**Key takeaway:** a clear diagram up front makes the later firewall and segmentation work much easier to reason about.

[View session notes →]()

---

### 🔜 Session 3 — pfSense Firewall
**Status:** Planned

**Objective:** Stand up pfSense as the lab's gateway and prove internal VMs can reach the internet *through* it while staying isolated from the host.

**Steps:**
- Install the pfSense VM with two network adapters (WAN and LAN)
- Configure it as the lab gateway and set initial firewall rules
- Move the Ubuntu VM behind the LAN interface

**Done when:** internal VMs reach the internet via pfSense, and the host network is unreachable from inside the lab.

---

### 🔜 Session 4 — Network Monitoring
**Status:** Planned

**Objective:** See what's actually crossing the wire and establish a baseline of "normal."

**Steps:**
- Install a monitoring tool (Security Onion or similar)
- Capture and analyse traffic passing through pfSense
- Baseline normal traffic, then generate test events to confirm detection works

**Done when:** normal traffic is baselined and a deliberate test event shows up in the monitoring tool.

---

### 🔜 Session 5 — Attack & Detect
**Status:** Planned

**Objective:** Run controlled attacks and learn to tell malicious traffic apart from normal traffic.

**Steps:**
- Use Kali Linux to run controlled attacks against lab targets
- Observe how that traffic appears in the monitoring tools
- Document what malicious activity looks like on the wire vs. normal activity

**Done when:** an attack can be traced end-to-end from Kali through pfSense to the detection tool.

---

### 🔜 Session 6 — Automation
**Status:** Planned

**Objective:** Cut out repetitive manual lab work with scripts.

**Steps:**
- Write scripts to automate backups, log parsing, or alerting
- Document what was automated and why

**Done when:** a previously manual task runs on its own and is documented.

---

## Skills Demonstrated

- **Virtualisation** — VirtualBox, VM networking modes
- **Network architecture design** — firewall, segmentation, NAT
- **Troubleshooting** — diagnosing addressing issues, reading scan output
- **Security tooling** — Nmap, Wireshark, WPScan
- **Documentation** — session journals with honest troubleshooting notes

---

*This lab is actively updated as sessions are completed. All notes include what broke and what didn't work along the way.*

