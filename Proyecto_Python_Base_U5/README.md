# Unidad 5 CLN - laboratorio completo y corregido

## Ejecutar en Windows
1. Instala **Python 3.11 o superior** desde python.org. Durante la instalación, marca la opción para agregar Python al PATH.
2. Extrae **todo el ZIP** en una carpeta nueva; no ejecutes directamente dentro del ZIP.
3. Abre `EJECUTAR_WINDOWS.bat` con doble clic. Se instalarán las dependencias automáticamente (se requiere Internet la primera vez).
4. El ejecutable aplica `ruff check --fix` y `ruff format` antes de verificar el estilo; así corrige automáticamente las importaciones `I001` y las modernizaciones `UP017` si reaparecen.
5. Si todo está bien, verás `TODO CORRECTO` y podrás abrir `htmlcov/index.html` para consultar la cobertura.

**Muy importante:** borra o deja de usar las carpetas descomprimidas de las versiones anteriores. Extrae este ZIP en una carpeta **nueva** para evitar la ejecución de archivos antiguos.

En Linux y macOS ejecuta `sh EJECUTAR_LINUX_MAC.sh`.

## Ejecución manual
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
ruff check --fix src tests cargar_datos_demo.py
ruff format src tests cargar_datos_demo.py
ruff check src tests cargar_datos_demo.py
pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80
```

## Contenido de la entrega
- `tests/test_csv_cases.py`: pruebas parametrizadas de CP01-CP12 usando `csv.DictReader`.
- `tests/test_additional_cases.py`: CP13-CP15, commit, rollback y seguridad.
- `src/domain.py`: corrección del CP08: confirmar dos veces lanza `OrderAlreadyConfirmed`.
- `MATRIZ_RESULTADOS.csv`: resultados esperados y observados.
- `EVIDENCIA_PRUEBAS.txt`: reporte de ejecución y cobertura.
- `.github/workflows/ci.yml`: validación automática con Ruff y pytest.
- CSV y SQLite de prueba originales y `cargar_datos_demo.py` para regenerar la base didáctica.

La prueba de repositorio usa SQLite en memoria. El archivo SQLite incluido es un dataset independiente; no se importa automáticamente. El rechazo del gateway se prueba con un `Mock`.

## Requisitos
Python >=3.11, acceso a internet para instalar dependencias y espacio de escritura en la carpeta extraída.


## Reporte académico basado en la guía U5 (entrega complementaria)

- `REPORTE_U5_Integracion_Pruebas_Calidad.docx`: informe editable con portada, E1–E9, tablas, reflexión de 176 palabras y pendientes reales.
- `REPORTE_U5_Integracion_Pruebas_Calidad.pdf`: copia para lectura e impresión.
- `tests/test_evidencias_guia.py`: 4 pruebas adicionales solicitadas por la guía (VIP y regular de 200, id=2/total=250/commit, rechazo de VIP 200 con cargo 170).
- `evidencias/E1-E7/`: registros de ejecución reales (Linux, Python 3.13.5), representaciones gráficas etiquetadas del resultado, y código usado para reproducir RED desde el ZIP original.
- `htmlcov/index.html`: reporte HTML generado, que muestra 100% de líneas de src/.
- `MATRIZ_PIA_PARA_COMPLETAR.csv`: 9 filas para las TRES reglas de negocio de la empresa del PIA; es una plantilla, no evidencia de pruebas ejecutadas.

**Última comprobación:** 37 pruebas aprobadas, 100% de cobertura de src/. Ruff no estuvo disponible para ejecutar en este entorno; debes validarlo en Windows cuando se instalen las dependencias.

**Pendientes que requieren tu intervención:** E8 exige ejecuciones reales de GitHub Actions (verde/roja/verde); E9 exige datos y reglas auténticas de tu propia empresa PIA, nueve casos ejecutables y su cobertura. No se inventaron capturas ni resultados de esas dos evidencias.

Para visualizar el reporte PDF no se requiere Python. Para correr el código sí se requiere Python 3.11 o superior.
