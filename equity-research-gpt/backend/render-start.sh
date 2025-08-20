#!/usr/bin/env bash
set -euo pipefail
cd api
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app
