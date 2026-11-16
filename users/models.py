"""Модель пользователя предметной области."""
from django.db import models


class User(models.Model):
    """Пользователь системы формирования списка покупок."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
    )

    def __str__(self):
        """Вернуть имя пользователя."""
        return self.name

    class Meta:
        """Сортировка и названия модели."""

        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
