"""Сохранение и загрузка данных проекта в JSON."""
import json
from pathlib import Path

from models.products import Product
from models.purchases import Purchase
from models.users import User


def _read_json(filename: Path) -> list:
    """Прочитать JSON-файл. При ошибке вернуть пустой список."""
    try:
        with filename.open(encoding="utf-8") as source:
            data = json.load(source)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return data


def _write_json(filename: Path, payload: list) -> None:
    """Записать данные в JSON-файл."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as target:
        json.dump(payload, target, ensure_ascii=False, indent=4)


def load_products(filename: Path) -> dict[int, Product]:
    """Загрузить товары из JSON-файла."""
    products = {}
    for item in _read_json(filename):
        product = Product.from_dict(item)
        products[product.id] = product
    return products


def save_products(filename: Path, products: dict[int, Product]) -> None:
    """Сохранить товары в JSON-файл."""
    payload = [product.to_dict() for product in products.values()]
    _write_json(filename, payload)


def load_users(filename: Path) -> dict[int, User]:
    """Загрузить пользователей из JSON-файла."""
    users = {}
    for item in _read_json(filename):
        user = User.from_dict(item)
        users[user.id] = user
    return users


def save_users(filename: Path, users: dict[int, User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    payload = [user.to_dict() for user in users.values()]
    _write_json(filename, payload)


def load_purchases(
    filename: Path,
    products: dict[int, Product],
    users: dict[int, User],
) -> list[Purchase]:
    """Загрузить позиции списка из JSON-файла."""
    purchases = []
    for item in _read_json(filename):
        purchases.append(Purchase.from_dict(item, products, users))
    return purchases


def save_purchases(filename: Path, purchases: list[Purchase]) -> None:
    """Сохранить позиции списка в JSON-файл."""
    payload = [purchase.to_dict() for purchase in purchases]
    _write_json(filename, payload)
