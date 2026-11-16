"""Тесты функций работы с товарами."""
import pytest

from models.products import (
    Product,
    add_product,
    check_product_quantity,
    filter_products_by_quantity,
    find_product,
    sort_products,
)


def test_add_product_assigns_next_id():
    """Новый товар получает следующий идентификатор."""
    products = {1: Product(1, "Молоко", 2)}
    product = add_product(products, "Хлеб", 1)
    assert product.id == 2
    assert products[2].name == "Хлеб"


def test_find_product_by_substring():
    """Поиск находит товар по части названия без учёта регистра."""
    products = {
        1: Product(1, "Молоко", 2),
        2: Product(2, "Хлеб", 1),
    }
    found = find_product(products, "мол")
    assert [item.name for item in found] == ["Молоко"]


def test_check_filter_and_sort_quantity():
    """Проверка, отбор и сортировка используют количество товара."""
    products = {
        1: Product(1, "Молоко", 2),
        2: Product(2, "Яйца", 10),
        3: Product(3, "Хлеб", 1),
    }
    assert check_product_quantity(products, 2, 10) is True
    assert check_product_quantity(products, 3, 2) is False
    filtered = filter_products_by_quantity(products, 2)
    assert {item.name for item in filtered} == {"Молоко", "Яйца"}
    sorted_products = sort_products(products)
    assert [item.quantity for item in sorted_products] == [1, 2, 10]


def test_missing_product_raises_key_error():
    """Отсутствующий товар не скрывается под ложным ответом."""
    with pytest.raises(KeyError):
        check_product_quantity({}, 1, 1)
