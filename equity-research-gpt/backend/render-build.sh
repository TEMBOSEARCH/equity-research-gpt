#!/usr/bin/env bash
set -euo pipefail
echo "[build] pwd=$(pwd)"
ls -la
cd api
echo "[build] now in $(pwd)"
python --version || true
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
