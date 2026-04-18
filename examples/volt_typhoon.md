# Volt Typhoon (2021–present, disclosed 2023–2024) — Authorization Context Analysis

## SKELETON

- Conducts extensive pre-compromise reconnaissance (FOFA, Shodan, Censys, victim-owned websites, OSINT on IT and network staff)
- Gains initial access by exploiting known and zero-day vulnerabilities in public-facing network appliances from Fortinet, Ivanti Connect Secure, NETGEAR, Citrix, and Cisco
- In one confirmed compromise, exploits CVE-2022-42475 on an unpatched FortiGate 300D perimeter firewall, including harvesting a domain administrator credential stored insecurely on the appliance itself
- Connects to victim networks via VPN sessions using harvested valid credentials, blending with legitimate remote-user traffic
- Operates entirely through Living Off the Land (LOTL) techniques — native Windows binaries such as `cmd`, `certutil`, `dnscmd`, `ldifde`, `makecab`, `net`, `netsh`, `nltest`, `netstat`, `ntdsutil`, `ping`, `PowerShell`, `quser`, `reg`, `systeminfo`, `tasklist`, `wevtutil`, `whoami`, `wmic`, `xcopy`
- Rarely deploys custom malware post-compromise; instead relies on hands-on-keyboard operator activity to avoid leaving artifacts
- Extracts the Active Directory database (`NTDS.dit`) via the Volume Shadow Copy Service, using `vssadmin` and `ntdsutil` through WMIC, to bypass live-volume file locking
- Cracks extracted password hashes offline (brute force, dictionary, rainbow tables) to recover plaintext credentials for any domain account
- Repeatedly re-extracts `NTDS.dit` from the same victim over time (observed: three extractions over four years at one victim, two extractions over nine months at another) to keep harvested credentials current
- Dumps LSASS process memory using a downloaded outdated copy of `comsvcs.dll` plus MiniDump, to capture in-memory credentials
- Deploys Mimikatz and Impacket (confirmed by incident responders and industry partners) for additional credential access
- Targets network administrator browser data — Chrome Local State (containing the AES encryption key) and Login Data — to recover plaintext passwords from browsers
- Targets personal email addresses of key network and IT staff, post-compromise, as an additional credential and intelligence source
- Moves laterally via RDP with harvested domain-admin credentials, and via PSExec using the `accepteula` command-line flag for unattended execution
- In one confirmed intrusion into a Water and Wastewater Systems entity, moved over nine months from initial access to file server, to domain controller, to Oracle Management Server, to VMware vCenter server adjacent to OT assets
- Interacts with saved PuTTY profiles on the vCenter server, including stored sessions for water treatment plants, water wells, an electrical substation, OT systems, and network security devices
- Tests access to domain-joined OT assets using vendor default credentials, and in some cases accesses OT systems whose credentials were recovered via NTDS.dit theft
- In one confirmed compromise, was positioned to move from one control system to a second control system
- Deploys FRP (Fast Reverse Proxy) clients (e.g., `BrightmetricAgent.exe`, `SMSvcService.exe`, UPX-packed) on victim corporate infrastructure for encrypted reverse-proxy C2
- Uses `netsh` PortProxy registry modifications on legitimate servers (e.g., a Paessler PRTG server) to convert them into intermediate proxies for C2 traffic
- Routes final C2 through multi-hop proxies composed of virtual private servers and compromised end-of-life SOHO routers (Cisco, NETGEAR) implanted with KV Botnet malware
- Selectively clears Windows Event Logs (Event ID 1102), system logs, and other artifacts to remove intrusion evidence
- Masquerades attacker file names as legitimate binaries (`ronf.exe` = renamed `rar.exe` for staging)
- Abstains from using compromised credentials outside the victim's normal working hours in some cases, to avoid anomaly-detection alerts
- Exfiltrates OT-facing documentation (SCADA diagrams, relay/switchgear documentation, construction drawings, facilities data) over SMB in zipped archives
- Once stable credential access is established, exhibits minimal activity — the objective is persistent presence, not immediate exploitation

## VIOLATIONS

- Assumes right to compromise internet-facing network appliances and inherit whatever trust relationships their defective credential storage exposes
- Assumes right to operate inside victim networks using exclusively the same tools the legitimate administrators use, laundering attacker activity through legitimate system behavior
- Assumes right to extract the entire credential store of the victim's identity provider (`NTDS.dit`) and re-extract it repeatedly over multiple years to maintain currency
- Assumes right to impersonate any user in the domain, including the most privileged accounts, by cracking harvested hashes offline where no network-side rate limiting applies
- Assumes right to dump process memory of the credential-handling component of the operating system (LSASS) to recover live session credentials
- Assumes right to read personal browser state belonging to named individual administrators, including stored passwords and browsing history, as a path into their personal identity perimeter
- Assumes right to target the personal email accounts of identified IT and network staff in order to cross from the work identity context into the personal identity context
- Assumes right to maintain stealthy, undetected presence on victim networks for periods measured in years, with the authoring agencies reporting dwell times of at least five years in some environments
- Assumes right to pre-position on IT networks not for intelligence-gathering but for forward-option disruption or destruction of operational technology, at a future moment of the attacker's choosing
- Assumes right to traverse from IT enclaves to OT-adjacent servers and to stage access to industrial control systems responsible for water treatment, electricity distribution, and other public-safety-critical functions
- Assumes right to compromise third-party SOHO routers belonging to uninvolved consumers and small businesses and weaponize them as attacker C2 infrastructure
- Assumes right to modify legitimate infrastructure (PRTG servers, network admin workstations) to serve attacker C2 purposes
- Assumes right to delete defender-side evidence of its own presence, denying the owner the ability to reconstruct what happened
- Assumes right to hold a *standing option* over victim infrastructure without ever having to exercise it — the authorization violation is the ongoing capability, not any single act
- Zero transparency to the victim at any layer; zero scope bound; no withdrawal mechanism; no consent at any tier of the multi-victim topology (appliance owners, router owners, IT staff, end users)

## CONTEXT THAT MAKES IT BAD

- U.S. CISA, NSA, and FBI assess with high confidence that Volt Typhoon actors are pre-positioning on U.S. critical infrastructure IT networks to enable disruption of OT functions in the event of crisis or conflict with the United States
- Confirmed compromises span Communications, Energy, Transportation Systems, and Water and Wastewater Systems sectors, including in Guam and other non-continental U.S. territories
- U.S. authoring agencies explicitly note the targeting pattern "is not consistent with traditional cyber espionage or intelligence gathering operations" — the violation is preparation for disruption, not collection
- Observed dwell times of at least five years in some victim environments; credentials were being repeatedly refreshed over multi-year windows, indicating the attacker treats access as a long-lived strategic asset rather than a tactical one
- Co-signed by NSA, FBI, DOE, EPA, TSA, Australian ACSC, Canadian CCCS, UK NCSC, and New Zealand NCSC — the scope is not a single-agency assessment but a Five Eyes + critical-infrastructure-partner consensus position
- Introduces a violation class not yet in the corpus: *Living-off-the-Land as authorization camouflage* — every individual operation performed by Volt Typhoon is something a legitimate administrator routinely does; the violation exists only in the actor's identity and the pattern across operations, not in any single technical primitive
- Introduces a second new violation class: *standing-option occupation* — the attacker holds an ongoing authorization they have granted themselves over the victim's infrastructure, choosing never to exercise it in most windows; the violation is the sustained capability, not any discrete harmful act
- Introduces a third new violation class: *personal-perimeter crossing* — targeting the personal email accounts of identified IT staff deliberately crosses from the employer-owned identity context into the employee-owned identity context, without any authorization relationship existing in the personal domain
- Owner-exclusion is systemic: conventional indicators of compromise are deliberately absent because no malware is used, defender behavioral baselines are often not mature enough to detect LOTL pattern deviations, and log deletion removes remaining post-hoc forensic ground truth
- Third-party collateral targeting at scale — the compromised SOHO routers (KV Botnet) are owned by uninvolved consumers and small businesses whose devices have been conscripted into nation-state C2 infrastructure without their knowledge; DOJ disrupted the botnet in early 2024 but the impressment pattern continues
- Sets a precedent for an ongoing campaign, not a discrete incident — Volt Typhoon intrusions remain active and new compromises continue to be discovered; remediation at any one victim does not terminate the campaign
- The choice to target water, energy, and transportation sectors signals intent to affect civilian public-safety outcomes in a future conflict — the violation is most fully understood as the cyber correlate of pre-positioning covert forces inside civilian infrastructure in advance of potential hostilities
- U.S. authoring agencies note that some victims are smaller organizations with limited cybersecurity capacity providing critical services to larger organizations or key geographic locations — the attacker deliberately chooses weaker nodes in the supply chain of criticality
- No meaningful consequences have been imposed on the PRC for this campaign; no international framework addresses standing-option occupation of civilian critical infrastructure as a distinct category of hostile state action

## REFERENCES

- CISA AA24-038A, "PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure" (2024-02-07, updated 2024-03-07)
- CISA AA23-144A, "People's Republic of China State-Sponsored Cyber Actor Living off the Land to Evade Detection" (2023-05-24, original Volt Typhoon disclosure)
- CISA MAR-10448362-1.v1, "Volt Typhoon" malware analysis report
- Joint guide "Identifying and Mitigating Living Off the Land Techniques" (CISA, NSA, FBI, and international partners)
- DOJ press release, "U.S. Government Disrupts Botnet People's Republic of China Used to Conceal Hacking of Critical Infrastructure" (KV Botnet disruption)
- Microsoft Threat Intelligence, "Volt Typhoon targets US critical infrastructure with living-off-the-land techniques" (2023-05-24)
- Secureworks, "Chinese Cyberespionage Group BRONZE SILHOUETTE Targets U.S. Government and Defense Organizations"
- Threat actor aliases: Vanguard Panda (CrowdStrike), BRONZE SILHOUETTE (Secureworks), Dev-0391 / Voltzite, UNC3236 (Mandiant), Insidious Taurus (Palo Alto)
