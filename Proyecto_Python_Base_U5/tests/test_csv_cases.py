"""Escenarios CP01-CP12 leídos de los CSV originales."""

import csv
from pathlib import Path

import pytest

from src.domain import CustomerHasDebt, Order, OrderAlreadyConfirmed

ROOT = Path(__file__).resolve().parents[1]


def read_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


ORDERS = {int(row["pedido_id"]): row for row in read_csv("pedidos_prueba.csv")}
CUSTOMERS = {int(row["cliente_id"]): row for row in read_csv("clientes_prueba.csv")}
CASES = [row for row in read_csv("casos_de_prueba.csv") if row["pedido_id"]]


@pytest.mark.parametrize("case", CASES, ids=[c["caso_id"] for c in CASES])
def test_csv_scenarios(case):
    row = ORDERS[int(case["pedido_id"])]
    customer = CUSTOMERS[int(row["cliente_id"])]
    assert row["es_vip"] == customer["es_vip"]
    assert float(row["deuda_cliente"]) == float(customer["deuda"])
    order = Order(float(row["total"]), vip=bool(int(row["es_vip"])), status=row["estado_inicial"])
    expected = case["resultado_esperado"]
    if case["caso_id"] == "CP08":
        with pytest.raises(OrderAlreadyConfirmed):
            order.confirm(customer_debt=float(row["deuda_cliente"]))
        assert order.status == "CONFIRMED"
    elif expected in ("CustomerHasDebt", "ValueError"):
        error = {"CustomerHasDebt": CustomerHasDebt, "ValueError": ValueError}[expected]
        with pytest.raises(error):
            order.confirm(customer_debt=float(row["deuda_cliente"]))
        assert order.status == "NEW"
    else:
        expected_status, expected_amount = expected.split(", cobro ")
        actual = order.confirm(customer_debt=float(row["deuda_cliente"]))
        assert order.status == expected_status
        assert actual == pytest.approx(float(expected_amount), abs=0.00001)


def test_second_confirmation_rejected_after_first_confirmation():
    order = Order(100, vip=True)
    assert order.confirm() == 85
    with pytest.raises(OrderAlreadyConfirmed):
        order.confirm()
    assert order.discount == 15
    assert order.status == "CONFIRMED"
