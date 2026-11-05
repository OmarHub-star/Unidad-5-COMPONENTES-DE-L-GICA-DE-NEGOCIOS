"""CP13-CP15 y ramas adicionales de seguridad y persistencia."""

from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.application import OrderService
from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine
from src.security import can_cancel


def test_cp13_payment_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError, match="payment rejected"):
        OrderService(gateway).checkout(Order(50))
    gateway.charge.assert_called_once_with(50)


def test_cp14_commit_visible_in_another_session():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(14, Order(120))
        session.commit()
    with Session(engine) as session:
        saved = session.scalar(select(OrderRow).where(OrderRow.id == 14))
        assert saved is not None
        assert saved.total == 120
        assert saved.status == "NEW"
    engine.dispose()


def test_cp15_rollback_not_visible_in_another_session():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(15, Order(120))
        session.flush()
        session.rollback()
    with Session(engine) as session:
        assert session.scalar(select(OrderRow).where(OrderRow.id == 15)) is None
    engine.dispose()


def test_admin_can_cancel_non_shipped_order():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    assert can_cancel("NEW", 1, 2, True, now - timedelta(days=30), now)


def test_owner_can_cancel_before_24_hour_limit():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=23), now)


def test_owner_cannot_cancel_at_24_hour_limit():
    now = datetime(2026, 1, 1, tzinfo=UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=24), now)


def test_security_uses_current_time_when_now_is_omitted():
    assert can_cancel("NEW", 1, 1, False, datetime.now(UTC))
