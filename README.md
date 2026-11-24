# Malware Analysis & Digital Forensics Lab (`sec04-malware-forensics`)

## Lab Topology (`malnet` Isolated Host-Only Network)
- **REMnux (`10.10.10.1`):** DNS/HTTP/HTTPS simulation (`INetSim`), packet capture (`tcpdump`), static triage, Ghidra reverse engineering, and YARA scanning.
- **WIN-ANALYST (`10.10.10.2`):** Isolated Windows detonation guest monitored with Sysinternals Process Monitor and Process Explorer (`CLEAN-BASELINE` snapshot restored post-execution).

## Repository Layout
- `static-analysis/` — Sample hashes, `strings`, `FLOSS` output, and Ghidra disassembly notes.
- `dynamic-analysis/` — `dynamic-traffic.pcap`, `inetsim-service.log`, `procmon-filtered.pml`, and `procmon-filtered.csv`.
- `tools/triage.py` — Standalone Python CLI utility for cryptographic hashing, Shannon entropy calculation, and regex IOC extraction.
- `yara/rules/` — Custom YARA detection rule (`sample_detection.yar`).
- `report/final-report.md` — Complete forensic analysis report and IOC summary.

## Usage
```bash
python3 tools/triage.py <path-to-sample>
yara yara/rules/sample_detection.yar <path-to-sample> 
