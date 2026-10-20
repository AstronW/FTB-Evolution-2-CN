#!/bin/sh
# Build from the repository folder, even when launched elsewhere.
set -eu
cd "$(dirname "$0")"
export PYTHONUTF8=1
for runner in python3 python; do
    if command -v "$runner" >/dev/null 2>&1 &&
        "$runner" -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
        exec "$runner" build.py
    fi
done
echo 'Python 3.8+ is required. Install it from https://www.python.org/downloads/ and run this script again.' >&2
exit 1
