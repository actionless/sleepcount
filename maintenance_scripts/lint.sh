#!/usr/bin/env bash
set -euo pipefail

TARGETS=(
	"sleepcount.py"
)
PYTHON=python3
TARGET_MODULE='sleepcount'

echo -e "\n== Running python compile:"
"$PYTHON" -O -m compileall "${TARGETS[@]}" \
| (\
	grep -v -e '^Listing' -e '^Compiling' || true \
)
echo ':: python compile passed ::'

echo -e "\n== Running python import:"
"$PYTHON" -c "from ${TARGET_MODULE} import cli"
echo -e ':: python import passed ::\n'

echo Flake8:
flake8 "${TARGETS[@]}"

echo PyLint:
pylint "${TARGETS[@]}" --score no

echo MyPy:
python -m mypy "${TARGETS[@]}"

	#./maintenance_scripts/vulture_whitelist.py \
echo Vulture:
vulture "${TARGETS[@]}" \
	--min-confidence=1 \
	--sort-by-size

echo '== GOOD!'
