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
"$PYTHON" -m flake8 "${TARGETS[@]}"

echo PyLint:
if [[ $("$PYTHON" --version | cut -d' ' -f2 | cut -d. -f2) -gt 9 ]] ; then
	"$PYTHON" -m pylint "${TARGETS[@]}" --score no
else
	"$PYTHON" -m pylint "${TARGETS[@]}" --score no --rcfile pylint_old.conf
fi

echo MyPy:
"$PYTHON" -m mypy "${TARGETS[@]}"

	#./maintenance_scripts/vulture_whitelist.py \
echo Vulture:
"$PYTHON" -m vulture "${TARGETS[@]}" \
	--min-confidence=1 \
	--sort-by-size

echo -e "\n== Print help message:"
"$PYTHON" "${TARGETS[0]}" --help

echo -e '\n== GOOD!'
