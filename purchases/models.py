"""Модель позиции списка покупок."""
from django.db import models

from products.models import Product
from users.models import User


class PurchaseQuerySet(models.QuerySet):
    """Выборки позиций по статусу и дате."""

    def active(self):
        """Вернуть активные позиции."""
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        """Вернуть вычеркнутые позиции."""
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        """Вернуть завершённые позиции."""
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        """Вернуть позиции за указанную дату."""
        return self.filter(purchase_date=selected_date)


class PurchaseManager(models.Manager.from_queryset(PurchaseQuerySet)):
    """Менеджер позиций списка покупок."""

    pass


class Purchase(models.Model):
    """Позиция списка покупок."""

    class Status(models.TextChoices):
        """Состояние позиции списка."""

        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

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
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус позиции",
    )

    objects = PurchaseManager()

    def cancel(self):
        """Вычеркнуть позицию и сохранить изменение."""
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

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
