"""Модель товара."""
from django.db import models


class Product(models.Model):
    """Товар списка покупок."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
    )

    def is_enough_for(self, needed):
        """Проверить, что количества товара достаточно."""
        return self.quantity >= needed

    def __str__(self):
        """Вернуть название товара."""
        return self.name

    class Meta:
        """Сортировка и названия модели."""

        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
