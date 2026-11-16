"""Тесты функций работы с товарами."""
import pytest

from products import (
    add_product,
    check_product_quantity,
    filter_products_by_quantity,
    find_product,
    sort_products,
)


def test_add_and_find_product():
    """Товар добавляется и находится по части названия."""
    products = {}
    add_product(products, "Молоко", 2)
    found = find_product(products, "мол")
    assert found[0]["name"] == "Молоко"
    assert found[0]["id"] == 1


def test_quantity_filter_and_sort():
    """Отбор и сортировка используют количество."""
    products = {
        1: {"id": 1, "name": "Молоко", "quantity": 2},
        2: {"id": 2, "name": "Яйца", "quantity": 10},
    }
    assert check_product_quantity(products, 2, 10) is True
    filtered = filter_products_by_quantity(products, 2)
    assert len(filtered) == 2
    ordered = sort_products(products)
    assert [item["quantity"] for item in ordered] == [2, 10]


def test_missing_product_raises_key_error():
    """Отсутствующий товар вызывает ошибку."""
    with pytest.raises(KeyError):
        check_product_quantity({}, 1, 1)
