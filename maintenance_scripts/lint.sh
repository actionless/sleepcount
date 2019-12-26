#!/usr/bin/env bash
set -euo pipefail

target="sleepcount.py"

echo Flake8:
flake8 "$target"

echo PyLint:
pylint "$target" --score no

echo MyPy:
python -m mypy "$target"

	#./maintenance_scripts/vulture_whitelist.py \
echo Vulture:
exec vulture "$target" \
	--min-confidence=1 \
	--sort-by-size

echo '== GOOD!'
