#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
  echo "Python venv not found. Create it first: python3 -m venv .venv"
  exit 1
fi

source .venv/bin/activate
export PYTHONPATH=.

python3 -c "from app.main import init_db; init_db()"
python3 scripts/seed_demo_data.py
python3 scripts/generate_demo_history.py
python3 scripts/show_history.py

echo "Demo data prepared."
echo "Graph path: artifacts/demo_price_history.png"
