"""Функции работы с позициями списка покупок."""
from datetime import date


def is_product_available(
    purchases: list[dict],
    product_id: int,
    purchase_date: date,
) -> bool:
    """Проверить, нет ли товара в списке на эту дату."""
    for purchase in purchases:
        same_product = purchase["product_id"] == product_id
        same_date = purchase["purchase_date"] == purchase_date
        if same_product and same_date:
            return False
    return True


def create_purchase(
    purchases: list[dict],
    product_id: int,
    purchase_date: date,
) -> dict:
    """Добавить товар в список на дату."""
    if not is_product_available(purchases, product_id, purchase_date):
        raise ValueError("Товар уже есть в списке на эту дату.")
    purchase_id = (
        max(item["id"] for item in purchases) + 1 if purchases else 1
    )
    purchase = {
        "id": purchase_id,
        "product_id": product_id,
        "purchase_date": purchase_date,
    }
    purchases.append(purchase)
    return purchase


def cancel_purchase(purchases: list[dict], purchase_id: int) -> None:
    """Удалить позицию из списка."""
    for index, purchase in enumerate(purchases):
        if purchase["id"] == purchase_id:
            del purchases[index]
            return
    raise KeyError(purchase_id)


def get_purchase_status(is_available: bool) -> str:
    """Вернуть текстовый статус товара."""
    if is_available:
        return "Товар можно добавить в список"
    return "Товар уже есть в списке на эту дату"
