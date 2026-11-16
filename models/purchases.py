"""Позиции списка покупок."""
from datetime import date

from models.products import Product
from models.users import User


class Purchase:
    """Позиция списка: товар, пользователь и дата покупки."""

    def __init__(
        self,
        purchase_id: int,
        product: Product,
        purchase_date: date,
        user: User,
        is_cancelled: bool = False,
    ) -> None:
        """Связать позицию с товаром и пользователем."""
        self.id = purchase_id
        self.product = product
        self.purchase_date = purchase_date
        self.user = user
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Вычеркнуть позицию из списка."""
        self.is_cancelled = True

    @property
    def status(self) -> str:
        """Вернуть текстовый статус позиции."""
        if self.is_cancelled:
            return "Позиция вычеркнута"
        return "Позиция в списке"

    def to_dict(self) -> dict:
        """Преобразовать позицию в словарь для JSON."""
        return {
            "id": self.id,
            "product_id": self.product.id,
            "user_id": self.user.id,
            "purchase_date": self.purchase_date.isoformat(),
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        products: dict[int, Product],
        users: dict[int, User],
    ) -> "Purchase":
        """Создать позицию из словаря JSON."""
        return cls(
            purchase_id=data["id"],
            product=products[data["product_id"]],
            purchase_date=date.fromisoformat(data["purchase_date"]),
            user=users[data["user_id"]],
            is_cancelled=data["is_cancelled"],
        )

    def __str__(self) -> str:
        """Вернуть товар, дату и пользователя позиции."""
        return (
            f"{self.product} — {self.purchase_date} ({self.user})"
        )


def is_product_available(
    purchases: list[Purchase],
    product_id: int,
    purchase_date: date,
) -> bool:
    """Проверить, можно ли добавить товар на дату.

    Вычеркнутая позиция дату не занимает.
    """
    for purchase in purchases:
        same_product = purchase.product.id == product_id
        same_date = purchase.purchase_date == purchase_date
        if same_product and same_date and not purchase.is_cancelled:
            return False
    return True


def create_purchase(
    purchases: list[Purchase],
    product: Product,
    user: User,
    purchase_date: date,
) -> Purchase:
    """Добавить товар в список, если на эту дату его ещё нет."""
    if not is_product_available(purchases, product.id, purchase_date):
        raise ValueError("Товар уже есть в списке на эту дату.")
    purchase_id = max(item.id for item in purchases) + 1 if purchases else 1
    purchase = Purchase(purchase_id, product, purchase_date, user)
    purchases.append(purchase)
    return purchase


def cancel_purchase(purchases: list[Purchase], purchase_id: int) -> None:
    """Вычеркнуть позицию по идентификатору."""
    for purchase in purchases:
        if purchase.id == purchase_id:
            purchase.cancel()
            return
    raise KeyError(purchase_id)


def get_purchase_status(is_available: bool) -> str:
    """Вернуть текстовый статус товара."""
    if is_available:
        return "Товар можно добавить в список"
    return "Товар уже есть в списке на эту дату"
