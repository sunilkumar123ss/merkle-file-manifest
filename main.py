"""Canonical file manifests with domain-separated Merkle hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
MAX_BYTES = 8 * 1024 * 1024

