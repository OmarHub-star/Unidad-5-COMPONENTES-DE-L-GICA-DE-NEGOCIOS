#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m ruff check --fix src tests cargar_datos_demo.py
python -m ruff format src tests cargar_datos_demo.py
python -m ruff check src tests cargar_datos_demo.py
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80
printf '\nPruebas aprobadas. Reporte HTML: htmlcov/index.html\n'
