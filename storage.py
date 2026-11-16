"""Сохранение и загрузка данных проекта в JSON."""
import json
from datetime import date
from pathlib import Path


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


def load_products(filename: Path) -> dict[int, dict]:
    """Загрузить товары из JSON-файла."""
    products = {}
    for item in _read_json(filename):
        products[item["id"]] = item
    return products


def save_products(filename: Path, products: dict[int, dict]) -> None:
    """Сохранить товары в JSON-файл."""
    _write_json(filename, list(products.values()))


def load_purchases(filename: Path) -> list[dict]:
    """Загрузить позиции списка из JSON-файла."""
    purchases = []
    for item in _read_json(filename):
        purchases.append({
            "id": item["id"],
            "product_id": item["product_id"],
            "purchase_date": date.fromisoformat(item["purchase_date"]),
        })
    return purchases


def save_purchases(filename: Path, purchases: list[dict]) -> None:
    """Сохранить позиции списка в JSON-файл."""
    payload = []
    for purchase in purchases:
        payload.append({
            "id": purchase["id"],
            "product_id": purchase["product_id"],
            "purchase_date": purchase["purchase_date"].isoformat(),
        })
    _write_json(filename, payload)
