"""Тесты позиций списка покупок."""
from datetime import date

import pytest

from models.products import Product
from models.purchases import (
    Purchase,
    cancel_purchase,
    create_purchase,
    get_purchase_status,
    is_product_available,
)
from models.users import User


def _product() -> Product:
    return Product(1, "Молоко", 2)


def _user() -> User:
    return User(1, "Анна", "anna@example.com")


def test_get_purchase_status():
    """Статус из начального сценария зависит от доступности товара."""
    assert get_purchase_status(True) == "Товар можно добавить в список"
    assert (
        get_purchase_status(False)
        == "Товар уже есть в списке на эту дату"
    )


def test_active_purchase_blocks_same_date():
    """Активная позиция занимает товар на свою дату."""
    product = _product()
    user = _user()
    purchase_date = date(2026, 9, 20)
    purchases = [
        Purchase(1, product, purchase_date, user),
    ]
    assert is_product_available(
        purchases,
        product.id,
        purchase_date,
    ) is False
    assert is_product_available(
        purchases,
        product.id,
        date(2026, 9, 21),
    ) is True


def test_cancelled_purchase_does_not_block():
    """Вычеркнутая позиция не мешает добавить товар на ту же дату."""
    product = _product()
    user = _user()
    purchase_date = date(2026, 9, 20)
    purchases = [
        Purchase(1, product, purchase_date, user, is_cancelled=True),
    ]
    assert is_product_available(purchases, product.id, purchase_date)
    created = create_purchase(purchases, product, user, purchase_date)
    assert created.status == "Позиция в списке"
    assert len(purchases) == 2


def test_create_purchase_rejects_duplicate():
    """Повторно добавить тот же товар на ту же дату нельзя."""
    product = _product()
    user = _user()
    purchase_date = date(2026, 9, 20)
    purchases = []
    create_purchase(purchases, product, user, purchase_date)
    with pytest.raises(ValueError):
        create_purchase(purchases, product, user, purchase_date)


def test_cancel_purchase():
    """Вычёркивание меняет статус существующей позиции."""
    product = _product()
    user = _user()
    purchases = [
        Purchase(4, product, date(2026, 9, 21), user),
    ]
    cancel_purchase(purchases, 4)
    assert purchases[0].is_cancelled is True
    assert purchases[0].status == "Позиция вычеркнута"
    with pytest.raises(KeyError):
        cancel_purchase(purchases, 99)
