"""Тесты сохранения JSON."""
from datetime import date

from storage import (
    load_products,
    load_purchases,
    save_products,
    save_purchases,
)


def test_storage_roundtrip(tmp_path):
    """Словари сохраняются в JSON и читаются обратно."""
    products = {1: {"id": 1, "name": "Молоко", "quantity": 2}}
    purchases = [{
        "id": 1,
        "product_id": 1,
        "purchase_date": date(2026, 9, 20),
    }]
    products_file = tmp_path / "products.json"
    purchases_file = tmp_path / "purchases.json"
    save_products(products_file, products)
    save_purchases(purchases_file, purchases)
    assert load_products(products_file)[1]["name"] == "Молоко"
    loaded = load_purchases(purchases_file)
    assert loaded[0]["purchase_date"] == date(2026, 9, 20)


def test_load_missing_file_returns_empty(tmp_path):
    """Отсутствующий файл не завершает загрузку ошибкой."""
    assert load_products(tmp_path / "missing.json") == {}
