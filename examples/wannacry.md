# WannaCry (May 2017) — Authorization Context Analysis

## SKELETON

- Propagates via SMBv1 remote code execution vulnerability (CVE-2017-0144, ETERNALBLUE)
- Installs DoublePulsar backdoor as staging implant before main payload delivery
- Scans local subnet and randomly generated public IPv4 addresses for SMBv1-exposed hosts
- Queries a hardcoded domain at startup; exits if the domain resolves ("kill switch" behavior)
- Enumerates local drives and network shares accessible by the infected host
- Encrypts files matching ~170 extension types using AES-128 per file, with per-file keys wrapped by an RSA-2048 public key
- Drops a ransom note (`@Please_Read_Me@.txt`) and a ransom UI (`@WanaDecryptor@.exe`) in each affected directory
- Deletes Volume Shadow Copies via `vssadmin delete shadows /all /quiet` to prevent local rollback
- Displays countdown timer and Bitcoin wallet addresses demanding ~$300 (increasing to ~$600) in BTC
- Stores the private RSA key encrypted with the operator's master key; offers partial file decryption as proof-of-capability
- Persists via scheduled task and registry Run key entries
- Propagates laterally to any reachable SMBv1 host within the kill-switch domain constraint
- Uses exploit code (ETERNALBLUE, DoublePulsar) previously leaked from NSA by the Shadow Brokers

## VIOLATIONS

- Assumes right to execute code on any reachable host exposing SMBv1, with zero user interaction
- Assumes right to weaponize a leaked nation-state exploit without the original developer's consent or the victim's ability to patch in time
- Assumes right to traverse and read any file on any mounted drive or accessible share
- Assumes right to permanently encrypt victim data and hold it hostage for cryptocurrency payment
- Assumes right to delete local rollback mechanisms (shadow copies) to eliminate recovery options
- Assumes right to offer a trust contract ("pay and recover") while operating infrastructure known to be unable to fulfill it reliably
- Assumes right to self-propagate across internal networks and arbitrary public IP ranges without any scope limit
- Assumes right to disrupt any organization reachable by the internet, including critical public services
- Assumes right to contain a single-point kill switch the operator did not actually control — ceding the operation's fate to whoever registered the domain first
- Zero authorization checks at any layer — no consent, no targeting discipline, no victim-class exclusions

## CONTEXT THAT MAKES IT BAD

- Crippled the UK National Health Service during active operation — ambulances diverted, surgeries cancelled, emergency care degraded across multiple NHS trusts
- Infected an estimated 200,000+ systems across 150 countries within 4 days; damages estimated at $4B+
- Payment infrastructure was broken — operators did not reliably deliver decryption keys even when ransoms were paid, exposing the ransom contract as partially fraudulent
- Weaponized NSA-developed exploit code (ETERNALBLUE) leaked via Shadow Brokers, establishing the precedent that hoarded nation-state capabilities leak and get repurposed
- Microsoft had released a patch (MS17-010) two months before the attack; the damage was concentrated on unpatched systems, revealing the scale of unmaintained SMBv1 exposure on the public internet
- Kill switch discovery (MalwareTech, Marcus Hutchins) showed the operators did not control their own tool's fate — a single researcher registering a domain globally halted propagation
- Attribution to Lazarus Group (North Korea) established that state actors use ransomware as a deniable revenue and chaos mechanism, not just as espionage
- Surfaces a new violation class: *hostage model built on a known-broken trust contract* — the attacker charges for a service they cannot reliably deliver, while the victim has no recourse
- Leaked-exploit supply chain becomes a visible attack surface class: every zero-day hoarded by a nation-state is a future mass-casualty incident waiting on a leak
- Demonstrates that internet-exposed legacy protocols (SMBv1) are a continuous global liability even when patches exist — the internet cannot be patched, only populated with patched hosts
