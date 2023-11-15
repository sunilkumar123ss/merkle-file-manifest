"""Canonical file manifests with domain-separated Merkle hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
MAX_BYTES = 8 * 1024 * 1024

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')

def merkle(entries):
    level = [hashlib.sha256(b'\x00' + canonical(row)).digest() for row in entries]
    if not level:
        return hashlib.sha256(b'\x02').hexdigest()
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [hashlib.sha256(b'\x01' + level[i] + level[i + 1]).digest() for i in range(0, len(level), 2)]
    return level[0].hex()
