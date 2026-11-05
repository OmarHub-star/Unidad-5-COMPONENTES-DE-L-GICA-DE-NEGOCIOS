"""Prueba RED ejecutada contra una copia SIN modificar del ZIP base de U5.

NO colocar en tests/ de la versión final: esta prueba está escrita para fallar
contra el código original y demostrar que todavía permite confirmar dos veces.
Para reproducir, extraer Proyecto_Python_Base_U5.zip en carpeta aparte,
copiar este archivo dentro de tests/ y ejecutar:
    python -m pytest tests/test_tdd_red_solo_codigo_base.py -v
"""
import pytest

from src.domain import Order


def test_cannot_confirm_twice():
    order = Order(100)
    order.confirm()
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()
