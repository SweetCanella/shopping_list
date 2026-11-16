"""Товары списка покупок."""


class Product:
    """Товар, который можно добавить в список покупок."""

    def __init__(self, product_id: int, name: str, quantity: int) -> None:
        """Сохранить идентификатор, название и количество товара."""
        self.id = product_id
        self.name = name
        self.quantity = quantity

    def is_enough_for(self, needed: int) -> bool:
        """Проверить, что количества товара достаточно."""
        return self.quantity >= needed

    def to_dict(self) -> dict:
        """Преобразовать товар в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Создать товар из словаря JSON."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            quantity=data["quantity"],
        )

    def __str__(self) -> str:
        """Вернуть название товара."""
        return self.name


def add_product(
    products: dict[int, Product],
    product_name: str,
    quantity: int,
) -> Product:
    """Добавить товар в словарь products."""
    product_id = max(products) + 1 if products else 1
    product = Product(product_id, product_name, quantity)
    products[product_id] = product
    return product


def find_product(
    products: dict[int, Product],
    query: str,
) -> list[Product]:
    """Найти товары по подстроке названия."""
    prepared_query = query.casefold()
    found = []
    for product in products.values():
        if prepared_query in product.name.casefold():
            found.append(product)
    return found


def check_product_quantity(
    products: dict[int, Product],
    product_id: int,
    min_quantity: int,
) -> bool:
    """Проверить количество товара."""
    product = products[product_id]
    return product.is_enough_for(min_quantity)


def filter_products_by_quantity(
    products: dict[int, Product],
    min_quantity: int,
) -> list[Product]:
    """Отобрать товары с количеством не меньше заданного."""
    return list(
        product
        for product in products.values()
        if product.is_enough_for(min_quantity)
    )


def sort_products(products: dict[int, Product]) -> list[Product]:
    """Отсортировать товары по количеству."""
    return sorted(
        products.values(),
        key=lambda product: product.quantity,
    )
