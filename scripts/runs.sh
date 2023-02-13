#!/usr/bin/env bash
set -e


echo "Revenue dash running"
python3 revenue_dash.py dashboard.conf 
echo "Revenue run complete"
