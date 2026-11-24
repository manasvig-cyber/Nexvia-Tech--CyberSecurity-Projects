#!/usr/bin/env python3
import argparse
import hashlib
import math
import re
import sys
from pathlib import Path


def file_hashes(data: bytes) -> dict:
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in freq if c)


def extract_iocs(data: bytes) -> dict:
    ascii_strings = re.findall(rb"[ -~]{5,}", data)
    wide_strings = re.findall(rb"(?:[ -~]\x00){5,}", data)
    decoded = [s.decode("ascii", errors="ignore") for s in ascii_strings] + [
        s.decode("utf-16le", errors="ignore") for s in wide_strings
    ]
    blob = "\n".join(decoded)

    url_pattern = r"https?://[^\s\"'<>]+"
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    domain_pattern = (
        r"\b(?:[a-zA-Z0-9-]+\.)+"
        r"(?:com|net|org|io|ru|cn|xyz|top|info|biz)\b"
    )
    reg_pattern = r"(?:HKEY_[A-Z_]+|HKLM|HKCU)\\[^\s\"']+"

    return {
        "urls": sorted(set(re.findall(url_pattern, blob))),
        "ips": sorted(set(re.findall(ip_pattern, blob))),
        "domains": sorted(set(re.findall(domain_pattern, blob))),
        "registry": sorted(set(re.findall(reg_pattern, blob, re.I))),
    }


def main():
    parser = argparse.ArgumentParser(description="CLI Malware Triage Utility")
    parser.add_argument("sample", help="Path to target binary")
    args = parser.parse_args()

    path = Path(args.sample)
    if not path.is_file():
        sys.exit(f"[!] File not found: {path}")

    data = path.read_bytes()
    hashes = file_hashes(data)
    entropy = shannon_entropy(data)
    iocs = extract_iocs(data)

    print(f"=== TRIAGE REPORT: {path.name} ({len(data)} bytes) ===")
    for k, v in hashes.items():
        print(f"{k.upper():<8}: {v}")
    print(f"ENTROPY : {entropy:.4f} / 8.0000")

    for category, items in iocs.items():
        print(f"\n[{category.upper()}] ({len(items)})")
        for item in items[:25]:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
