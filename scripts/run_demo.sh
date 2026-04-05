#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m app.main &
APP_PID=$!
sleep 3
kill "$APP_PID" || true

python3 scripts/seed_demo_data.py
python3 scripts/generate_demo_history.py

echo "Demo data prepared."
echo "Graph path: artifacts/demo_price_history.png"
