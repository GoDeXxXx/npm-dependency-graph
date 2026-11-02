#!/bin/sh
# модульные тесты
cd "$(dirname "$0")" || exit 1
python3 -m unittest discover -s python -p "test_*.py" -v
