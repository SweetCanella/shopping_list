"""Консольное приложение системы формирования списка покупок."""
from pathlib import Path

from products import (
    add_product,
    check_product_quantity,
    find_product,
)
from purchases import (
    cancel_purchase,
    create_purchase,
    get_purchase_status,
    is_product_available,
)
from storage import (
    load_products,
    load_purchases,
    save_products,
    save_purchases,
)
from utils import input_date, input_int

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
PURCHASES_FILE = BASE_DIR / "data" / "purchases.json"


def show_products(products: dict[int, dict]) -> None:
    """Вывести список товаров."""
    if not products:
        print("Товары отсутствуют.")
        return
    for product in products.values():
        print(
            f"{product['id']}. {product['name']}: "
            f"{product['quantity']}"
        )


def show_purchases(
    products: dict[int, dict],
    purchases: list[dict],
) -> None:
    """Вывести список покупок."""
    if not purchases:
        print("Список покупок пуст.")
        return
    for purchase in purchases:
        product = products[purchase["product_id"]]
        print(
            f"{purchase['id']}. {product['name']}, "
            f"{purchase['purchase_date']:%d.%m.%Y}"
        )


def _find_exact_product(products: dict[int, dict], name: str) -> dict | None:
    """Найти товар по точному названию."""
    for product in find_product(products, name):
        if product["name"].casefold() == name.casefold():
            return product
    return None


def search_products(products: dict[int, dict]) -> None:
    """Найти товары по части названия."""
    query = input("Название товара: ").strip()
    found = find_product(products, query)
    if not found:
        print("Товары не найдены.")
        return
    for product in found:
        print(
            f"{product['id']}. {product['name']}: "
            f"{product['quantity']}"
        )


def check_quantity(products: dict[int, dict]) -> None:
    """Проверить, хватает ли количества товара."""
    name = input("Название товара: ").strip()
    product = _find_exact_product(products, name)
    if product is None:
        print("Товар не найден.")
        return
    needed = input_int("Нужное количество: ")
    if check_product_quantity(products, product["id"], needed):
        print("Количества достаточно.")
        return
    print("Количества недостаточно.")


def check_availability(
    products: dict[int, dict],
    purchases: list[dict],
) -> None:
    """Проверить, свободен ли товар на дату."""
    name = input("Название товара: ").strip()
    product = _find_exact_product(products, name)
    if product is None:
        print("Товар не найден.")
        return
    purchase_date = input_date("Дата: ")
    is_available = is_product_available(
        purchases,
        product["id"],
        purchase_date,
    )
    print(get_purchase_status(is_available))


def add_new_product(products: dict[int, dict]) -> None:
    """Добавить новый товар и сохранить его."""
    name = input("Название товара: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return
    quantity = input_int("Количество: ")
    if quantity < 0:
        print("Количество не может быть отрицательным.")
        return
    add_product(products, name, quantity)
    save_products(PRODUCTS_FILE, products)
    print("Товар добавлен.")


def add_to_list(
    products: dict[int, dict],
    purchases: list[dict],
) -> None:
    """Добавить товар в список покупок."""
    name = input("Название товара: ").strip()
    product = _find_exact_product(products, name)
    if product is None:
        print("Товар не найден.")
        return
    purchase_date = input_date("Дата: ")
    try:
        create_purchase(purchases, product["id"], purchase_date)
    except ValueError as error:
        print(error)
        return
    save_purchases(PURCHASES_FILE, purchases)
    print("Позиция добавлена.")


def cross_out(purchases: list[dict]) -> None:
    """Удалить позицию из списка."""
    purchase_id = input_int("Номер позиции: ")
    try:
        cancel_purchase(purchases, purchase_id)
    except KeyError:
        print("Позиция не найдена.")
        return
    save_purchases(PURCHASES_FILE, purchases)
    print("Позиция удалена.")


def print_menu() -> None:
    """Вывести меню приложения."""
    print()
    print("=== Система формирования списка покупок ===")
    print("1. Показать товары")
    print("2. Найти товар по названию")
    print("3. Проверить количество")
    print("4. Проверить, свободен ли товар на дату")
    print("5. Добавить товар в список")
    print("6. Удалить позицию")
    print("7. Показать список покупок")
    print("8. Добавить товар")
    print("0. Выход")


def main() -> None:
    """Запустить меню приложения."""
    products = load_products(PRODUCTS_FILE)
    purchases = load_purchases(PURCHASES_FILE)
    actions = {
        "1": lambda: show_products(products),
        "2": lambda: search_products(products),
        "3": lambda: check_quantity(products),
        "4": lambda: check_availability(products, purchases),
        "5": lambda: add_to_list(products, purchases),
        "6": lambda: cross_out(purchases),
        "7": lambda: show_purchases(products, purchases),
        "8": lambda: add_new_product(products),
    }
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("Работа завершена.")
            break
        action = actions.get(choice)
        if action is None:
            print("Нет такого пункта меню.")
            continue
        action()


if __name__ == "__main__":
    main()
