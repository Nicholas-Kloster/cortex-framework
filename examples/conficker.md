# Conficker Worm (2008) — Authorization Context Analysis

## SKELETON

- Exploits MS08-067 (Windows Server Service buffer overflow) for remote code execution
- Disables Windows Automatic Update service
- Disables Windows Security Center and Windows Defender
- Blocks DNS resolution for security vendor domains
- Downloads and executes arbitrary code from generated domain names (DGA)
- Generates pseudo-random domain names daily using date as seed (Domain Generation Algorithm)
- Propagates via network shares using password brute-force
- Propagates via removable media (autorun.inf injection)
- Patches MS08-067 on infected hosts to block competing malware
- Establishes peer-to-peer C2 network across infected hosts
- Polls generated domains for updated payload instructions
- Enumerates and maps local network topology

## VIOLATIONS

- Assumes right to exploit OS vulnerability to gain execution without any user interaction
- Assumes right to disable host security mechanisms (Defender, Security Center, Windows Update)
- Assumes right to modify DNS resolution behavior system-wide
- Assumes right to block owner's access to security resources and patches
- Assumes right to brute-force credentials on network shares belonging to other systems
- Assumes right to write to removable media and modify autorun behavior
- Assumes right to establish persistent outbound C2 communication
- Assumes right to map and traverse the local network
- Assumes right to download and execute arbitrary remote code at attacker's direction
- Assumes right to modify OS internals to maintain exclusive infection (patches vulnerability for self-protection)
- Zero user interaction required for propagation after initial infection vector
- Actively works to prevent owner from regaining control (update/AV blocking)

## CONTEXT THAT MAKES IT BAD

- Infection requires zero user consent — exploits unpatched systems without interaction
- Systematically removes the owner's ability to detect or remediate the infection
- Blocking security updates and AV domains leaves the host permanently degraded even post-removal
- DGA-based C2 makes takedown exceptionally difficult — attacker rotates domains faster than defenders can block
- Brute-forcing network shares extends unauthorized access to systems beyond the originally infected host
- Peer-to-peer C2 eliminates single point of failure — no central server to shut down
- Estimated 9–15 million machines infected across government, military, business, and consumer systems
- Patching MS08-067 on infected hosts demonstrates deliberate owner-exclusion: attacker maintains sole access
- Removable media propagation jumps air-gapped or network-isolated systems
- Full network topology mapping gives attacker persistent intelligence about victim infrastructure
- Represents a platform, not just a worm — designed to maintain a controllable botnet, not just spread
