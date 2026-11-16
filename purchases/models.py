"""Модель позиции списка покупок."""
from django.db import models

from products.models import Product
from users.models import User


class Purchase(models.Model):
    """Позиция списка покупок."""

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchases",
        verbose_name="Товар",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="purchases",
        verbose_name="Пользователь",
    )
    purchase_date = models.DateField(
        verbose_name="Дата покупки",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Позиция вычеркнута",
    )

    def cancel(self):
        """Вычеркнуть позицию и сохранить изменение."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        """Вернуть товар, дату и пользователя."""
        return (
            f"{self.product} — {self.purchase_date} ({self.user})"
        )

    class Meta:
        """Сортировка и названия модели."""

        ordering = ["purchase_date", "pk"]
        verbose_name = "Позиция списка"
        verbose_name_plural = "Позиции списка"
