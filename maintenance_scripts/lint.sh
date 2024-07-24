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
if [[ $("$PYTHON" --version | cut -d' ' -f2 | cut -d. -f2) -gt 9 ]] ; then
	pylint "${TARGETS[@]}" --score no
else
	pylint "${TARGETS[@]}" --score no --rcfile pylint_old.conf
fi

echo MyPy:
python -m mypy "${TARGETS[@]}"

	#./maintenance_scripts/vulture_whitelist.py \
echo Vulture:
vulture "${TARGETS[@]}" \
	--min-confidence=1 \
	--sort-by-size

echo '== GOOD!'
