"""Casos complementarios exigidos por la guía del laboratorio U5."""

from unittest.mock import Mock

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.application import OrderService
from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


def test_vip_200_discount_170():
    order = Order(200, vip=True)
    assert order.confirm() == 170
    assert order.status == "CONFIRMED"


def test_regular_200_total_200():
    order = Order(200)
    assert order.confirm() == 200
    assert order.status == "CONFIRMED"


def test_repository_250_id_2_commit():
    engine = make_engine()
    try:
        with Session(engine) as session:
            SqlOrderRepository(session).save(2, Order(250))
            session.commit()
        with Session(engine) as session:
            saved = session.scalar(select(OrderRow).where(OrderRow.id == 2))
            assert saved is not None
            assert saved.id == 2
            assert saved.total == 250
            assert saved.status == "NEW"
    finally:
        engine.dispose()


def test_gateway_rejects_vip_200_charge_170():
    gateway = Mock()
    gateway.charge.return_value = False
    order = Order(200, vip=True)

    with pytest.raises(RuntimeError, match="payment rejected"):
        OrderService(gateway).checkout(order)

    gateway.charge.assert_called_once_with(170)
    # Riesgo de consistencia por diseño: el pedido queda CONFIRMED pese al rechazo.
    assert order.status == "CONFIRMED"
