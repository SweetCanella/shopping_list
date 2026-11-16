"""Начальный сценарий системы формирования списка покупок."""
from datetime import date

product_name = "Молоко"
quantity = 2
purchase_date = date(2026, 9, 20)
is_available = True


def get_purchase_status(is_available):
    """Вернуть текстовый статус товара."""
    if is_available:
        return "Товар можно добавить в список"
    return "Товар уже есть в списке на эту дату"


def format_quantity(quantity):
    """Преобразовать количество товара в текст."""
    return str(quantity) + " шт."


def can_add_product(is_available, quantity):
    """Проверить, можно ли добавить товар в список."""
    if not is_available:
        return False
    if quantity > 0:
        return True
    return False


print("Товар: " + product_name)
print("Количество: " + format_quantity(quantity))
print("Дата: " + str(purchase_date))
print(get_purchase_status(is_available))
if can_add_product(is_available, quantity):
    print("Товар будет добавлен в список")
else:
    print("Товар не будет добавлен в список")
