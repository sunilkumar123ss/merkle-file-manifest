# Merkle file manifest

Detect directory changes using canonical file leaves and a reproducible Merkle root.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

The manifest records each relative file path, byte length, and SHA-256. Leaves hash canonical JSON with a leaf prefix; internal nodes use a different prefix and duplicate the last child when a level has odd length. Comparison identifies added, removed, and changed paths.

## Use in Python

```python
from main import build, compare

# Use an existing stable directory; keep manifests outside that directory.
before = build('documents')
# After an intentional document edit:
after = build('documents')
changes = compare(before, after)
```

## Design limits

This checks a stable local directory snapshot, not a live filesystem under concurrent writes. Symlinks are rejected and each file is limited to 8 MiB. The root is not signed: authenticity requires keeping a trusted root separately. Store exported manifests outside the scanned tree to avoid self-inclusion.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
