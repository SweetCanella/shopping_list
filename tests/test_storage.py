"""Тесты сохранения и загрузки JSON."""
from datetime import date

from models.products import Product
from models.purchases import Purchase
from models.users import User
from storage import (
    load_products,
    load_purchases,
    load_users,
    save_products,
    save_purchases,
    save_users,
)


def test_storage_roundtrip(tmp_path):
    """Объекты сохраняются в JSON и читаются обратно."""
    products = {1: Product(1, "Молоко", 2)}
    users = {1: User(1, "Анна", "anna@example.com")}
    purchases = [
        Purchase(1, products[1], date(2026, 9, 20), users[1]),
    ]
    products_file = tmp_path / "products.json"
    users_file = tmp_path / "users.json"
    purchases_file = tmp_path / "purchases.json"

    save_products(products_file, products)
    save_users(users_file, users)
    save_purchases(purchases_file, purchases)

    loaded_products = load_products(products_file)
    loaded_users = load_users(users_file)
    loaded_purchases = load_purchases(
        purchases_file,
        loaded_products,
        loaded_users,
    )

    assert str(loaded_products[1]) == "Молоко"
    assert loaded_products[1].quantity == 2
    assert loaded_users[1].email == "anna@example.com"
    assert loaded_purchases[0].purchase_date == date(2026, 9, 20)
    assert loaded_purchases[0].product.name == "Молоко"


def test_load_missing_file_returns_empty(tmp_path):
    """Отсутствующий файл не завершает загрузку ошибкой."""
    assert load_products(tmp_path / "missing.json") == {}
