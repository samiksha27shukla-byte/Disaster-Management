#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m pip install -r requirements.txt
python -m src.validate_data
python run_demo.py
echo "Launch dashboard with: streamlit run app/dashboard.py"
