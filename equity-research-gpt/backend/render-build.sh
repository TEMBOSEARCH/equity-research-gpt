#!/usr/bin/env bash
set -euo pipefail
echo "[build] pwd=$(pwd)"
echo "[build] listing repo root"; ls -la
cd backend/api
echo "[build] pwd=$(pwd)"
python --version || true
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
