"""Тесты позиций списка покупок."""
from datetime import date

import pytest

from purchases import (
    cancel_purchase,
    create_purchase,
    get_purchase_status,
    is_product_available,
)


def test_get_purchase_status():
    """Статус из начального сценария сохранён."""
    assert get_purchase_status(True) == "Товар можно добавить в список"
    assert (
        get_purchase_status(False)
        == "Товар уже есть в списке на эту дату"
    )


def test_create_and_cancel_purchase():
    """Позиция создаётся и удаляется из списка."""
    purchases = []
    purchase_date = date(2026, 9, 20)
    created = create_purchase(purchases, 1, purchase_date)
    assert is_product_available(purchases, 1, purchase_date) is False
    with pytest.raises(ValueError):
        create_purchase(purchases, 1, purchase_date)
    cancel_purchase(purchases, created["id"])
    assert purchases == []
    with pytest.raises(KeyError):
        cancel_purchase(purchases, created["id"])
