"""Функции работы с товарами."""


def add_product(
    products: dict[int, dict],
    product_name: str,
    quantity: int,
) -> None:
    """Добавить товар в словарь products."""
    product_id = max(products) + 1 if products else 1
    products[product_id] = {
        "id": product_id,
        "name": product_name,
        "quantity": quantity,
    }


def find_product(
    products: dict[int, dict],
    query: str,
) -> list[dict]:
    """Найти товары по подстроке названия."""
    prepared_query = query.casefold()
    found = []
    for product in products.values():
        if prepared_query in product["name"].casefold():
            found.append(product)
    return found


def check_product_quantity(
    products: dict[int, dict],
    product_id: int,
    min_quantity: int,
) -> bool:
    """Проверить количество товара."""
    product = products[product_id]
    return product["quantity"] >= min_quantity


def filter_products_by_quantity(
    products: dict[int, dict],
    min_quantity: int,
) -> list[dict]:
    """Отобрать товары по количеству."""
    return list(
        product
        for product in products.values()
        if product["quantity"] >= min_quantity
    )


def sort_products(products: dict[int, dict]) -> list[dict]:
    """Отсортировать товары по количеству."""
    return sorted(
        products.values(),
        key=lambda product: product["quantity"],
    )
