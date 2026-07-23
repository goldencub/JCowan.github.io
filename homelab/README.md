Home Lab — Virtualised Network & Security Environment

A VirtualBox home lab covering firewalls, subnetting, and network monitoring — built from scratch, documented as it breaks.

This lab is a hands-on environment for practising real networking and security skills outside the classroom. Every session is documented including what went wrong and how it was diagnosed.

Lab Architecture
Component	Role
Host Machine	Windows 11, running VirtualBox
pfSense VM	Firewall and router between internal lab and host network
Ubuntu VM	Internal client machine, primary lab workstation
Kali Linux VM	Offensive security and pen-testing (planned)
Windows Server VM	Target machine for security testing (planned)

The lab is designed so all internal VMs sit behind pfSense on an isolated virtual network. pfSense acts as the gateway — the same role a physical firewall plays in a real network. Traffic from the internal VMs must pass through pfSense to reach the outside world.

Sessions
✅ Session 1 — Ubuntu VM Setup

Date: 20/07/2026

Installed Ubuntu Server on VirtualBox and confirmed internet connectivity. Discovered the VM received a 10.0.2.15 address rather than a 192.168.x.x address — diagnosed this as VirtualBox NAT mode creating its own private network inside the host machine. Documented the NAT traffic flow: VM → VirtualBox router → host machine's real IP → internet.

View session notes →

✅ Session 2 — GitHub Repository & Network Diagram

Date: 23/07/2026

Set up the GitHub portfolio repository and documented Session 1 findings. Designed the target lab architecture as a network diagram showing the relationships between host, hypervisor, pfSense, and internal VMs.

View session notes →

🔜 Session 3 — pfSense Firewall

Install pfSense VM with two network adapters (WAN and LAN). Configure as the lab's gateway, set firewall rules, and verify internal VMs can reach the internet through pfSense while being isolated from the host network.

🔜 Session 4 — Network Monitoring

Install a monitoring tool (Security Onion or similar) to capture and analyse traffic passing through pfSense. Baseline normal traffic, then generate test events to verify detection.

🔜 Session 5 — Attack & Detect

Use Kali Linux to run controlled attacks against lab targets. Observe how the traffic appears in monitoring tools. Document what malicious activity looks like on the wire versus normal traffic.

🔜 Session 6 — Automation

Write scripts to automate repetitive lab tasks — backups, log parsing, or alerting. Document what was automated and why.

Skills Demonstrated
Virtualisation (VirtualBox, VM networking modes)
Network architecture design (firewall, segmentation, NAT)
Troubleshooting (diagnosing addressing issues, reading scan output)
Security tooling (Nmap, Wireshark, WPScan)
Documentation (session journals with honest troubleshooting notes)

Sessions are added as completed. All notes also include what broke/didn't work
