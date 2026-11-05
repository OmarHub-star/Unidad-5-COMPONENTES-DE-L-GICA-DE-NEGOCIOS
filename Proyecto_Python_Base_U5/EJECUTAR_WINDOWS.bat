@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON=py -3"
) else (
    set "PYTHON=python"
)

%PYTHON% -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
if errorlevel 1 goto python_error

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto error
)

set "VENV_PYTHON=.venv\Scripts\python.exe"
echo Instalando dependencias...
"%VENV_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Corrigiendo automaticamente importaciones y estilo con Ruff...
"%VENV_PYTHON%" -m ruff check --fix src tests cargar_datos_demo.py
if errorlevel 1 goto lint_error
"%VENV_PYTHON%" -m ruff format src tests cargar_datos_demo.py
if errorlevel 1 goto lint_error
"%VENV_PYTHON%" -m ruff check src tests cargar_datos_demo.py
if errorlevel 1 goto lint_error

echo.
echo Ejecutando todas las pruebas y calculando cobertura...
"%VENV_PYTHON%" -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80
if errorlevel 1 goto error

echo.
echo TODO CORRECTO: Ruff y todas las pruebas aprobaron.
echo Reporte de cobertura: htmlcov\index.html
pause
exit /b 0

:lint_error
echo.
echo ERROR DE ESTILO: Ruff encontro un problema que no pudo corregirse.
echo Envia una captura del mensaje completo.
pause
exit /b 1

:python_error
echo.
echo ERROR: instala Python 3.11 o superior desde python.org y ejecuta otra vez.
pause
exit /b 1

:error
echo.
echo ERROR: revisa el mensaje anterior. Puede faltar acceso a Internet o alguna dependencia.
pause
exit /b 1
