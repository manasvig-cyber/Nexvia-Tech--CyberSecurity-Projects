# Malware Forensic Analysis Report

## 1. Executive Summary
A 64-bit Windows GUI binary (`3797d5082f3612a2493ce6430ed09a61922573f6871401f95b0d2e735a12ada1.exe`, 660,480 bytes) was analyzed in an isolated dual-VM lab (`malnet`: REMnux `10.10.10.1` and `WIN-ANALYST` `10.10.10.2`). Static triage, Ghidra reverse engineering, and dynamic behavioral monitoring indicate host reconnaissance and external IP geolocation profiling via `pro.ip-api.com`.

## 2. Sample Identification & Hashes
| Attribute | Value |
| :--- | :--- |
| **Filename** | `3797d5082f3612a2493ce6430ed09a61922573f6871401f95b0d2e735a12ada1.exe` |
| **File Size** | 660,480 bytes |
| **MD5** | `34e486e9bbc34d8084940d7694deb528` |
| **SHA-1** | `b7e2acec6c1908f28c65214a9baf1409eb3788ff` |
| **SHA-256** | `3797d5082f3612a2493ce6430ed09a61922573f6871401f95b0d2e735a12ada1` |
| **Shannon Entropy** | `6.3830 / 8.0000` |

## 3. Static & Reverse Engineering Findings
* **String Deobfuscation:** Identified string-decoding routine `mw_decode_strings` at virtual address `0x140048e0c` in Ghidra.
* **Embedded Network Indicators:** Automated extraction via `tools/triage.py` recovered an authenticated geolocation query URL (`https://pro.ip-api.com/line/?key=QPVvv1rHQJD2pd2&fields=25948155`) and domain reference `BreakingSecurity.net`.

## 4. Dynamic Behavioral & Network Analysis
* **Execution Context:** Spawned under `explorer.exe` (`PID 7132` / `PID 8944`) on `WIN-ANALYST` (`10.10.10.2`).
* **Network Telemetry:** Captured in `dynamic-traffic.pcap` and `inetsim-service.log`, showing DNS resolution requests and outbound HTTPS (`TCP/443`) connection attempts intercepted by INetSim (`sslv3 alert certificate unknown`).
* **Host Activity:** Filtered Process Monitor logs saved in `procmon-filtered.pml` and `procmon-filtered.csv`.

## 5. Indicators of Compromise (IOCs)
* **SHA-256:** `3797d5082f3612a2493ce6430ed09a61922573f6871401f95b0d2e735a12ada1`
* **URL:** `https://pro.ip-api.com/line/?key=QPVvv1rHQJD2pd2&fields=25948155`
* **Domains:** `pro.ip-api.com`, `BreakingSecurity.net`

## 6. Artifact Manifest
* `static-analysis/` — Sample hashes, strings, FLOSS output, and Ghidra analysis screenshots.
* `dynamic-analysis/` — `dynamic-traffic.pcap`, `inetsim-service.log`, `procmon-filtered.pml`, `procmon-filtered.csv`, and Wireshark captures.
* `tools/triage.py` — Standalone CLI triage utility for hashing, entropy calculation, and regex IOC extraction.
* `report/final-report.md` — Consolidated forensic analysis report.
