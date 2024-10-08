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

def build(directory):
    base = Path(directory).resolve()
    if not base.is_dir():
        raise ValueError('Directory does not exist')
    entries = []
    for path in sorted(base.rglob('*'), key=lambda entry: entry.relative_to(base).as_posix()):
        if path.is_symlink():
            raise ValueError('Symlinks are unsupported')
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError('Only regular files are supported')
        if path.stat().st_size > MAX_BYTES:
            raise ValueError('File exceeds 8 MiB')
        data = path.read_bytes()
        if len(data) > MAX_BYTES:
            raise ValueError('File exceeds 8 MiB')
        entries.append({'path': path.relative_to(base).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return {'format': 1, 'entries': entries, 'root': merkle(entries)}
