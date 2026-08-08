#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Zephyr: Installing dependencies ==="
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "=== Zephyr: Verifying imports ==="
python3 -c 'import flask; import flask_sqlalchemy; import faker; import models; print("All imports OK.")'

echo ""
echo "=== Zephyr: Running seed ==="
python3 seed.py

echo ""
echo "=== Setup complete ==="
echo "Run: python3 app.py"
