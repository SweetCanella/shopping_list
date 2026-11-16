"""Проверки статусов позиций списка покупок."""
from datetime import date

from django.test import TestCase
from django.urls import reverse

from products.models import Product
from purchases.models import Purchase
from users.models import User


class PurchaseStatusTests(TestCase):
    """Статус позиции, доступность товара и статистика."""

    def setUp(self):
        """Подготовить товар и пользователя."""
        self.product = Product.objects.create(
            name="Молоко",
            quantity=2,
        )
        self.user = User.objects.create(
            name="Анна",
            email="anna@example.com",
        )
        self.selected_date = date(2026, 9, 20)

    def _purchase(self, status, purchase_date=None):
        """Создать позицию с заданным статусом."""
        return Purchase.objects.create(
            product=self.product,
            user=self.user,
            purchase_date=purchase_date or self.selected_date,
            status=status,
        )

    def test_manager_returns_each_status(self):
        """Методы менеджера разделяют три состояния."""
        self._purchase(Purchase.Status.ACTIVE)
        self._purchase(
            Purchase.Status.CANCELLED,
            date(2026, 9, 21),
        )
        self._purchase(
            Purchase.Status.COMPLETED,
            date(2026, 9, 22),
        )
        self.assertEqual(Purchase.objects.active().count(), 1)
        self.assertEqual(Purchase.objects.cancelled().count(), 1)
        self.assertEqual(Purchase.objects.completed().count(), 1)
        self.assertEqual(
            Purchase.objects.for_date(self.selected_date).count(),
            1,
        )

    def test_cancelled_and_completed_do_not_block(self):
        """Товар занят только активной позицией на эту дату."""
        self._purchase(Purchase.Status.CANCELLED)
        self._purchase(
            Purchase.Status.COMPLETED,
            date(2026, 9, 21),
        )
        response = self.client.get(
            reverse("products:available"),
            {"date": "2026-09-20"},
        )
        self.assertContains(response, "Молоко")
        self._purchase(Purchase.Status.ACTIVE)
        response = self.client.get(
            reverse("products:available"),
            {"date": "2026-09-20"},
        )
        self.assertNotContains(response, "Молоко")

    def test_statistics_count_each_status(self):
        """Статистика считает активные, вычеркнутые и завершённые."""
        self._purchase(Purchase.Status.ACTIVE)
        self._purchase(
            Purchase.Status.CANCELLED,
            date(2026, 9, 21),
        )
        self._purchase(
            Purchase.Status.COMPLETED,
            date(2026, 9, 22),
        )
        response = self.client.get(reverse("purchases:statistics"))
        self.assertContains(response, "Активных позиций: 1")
        self.assertContains(response, "Вычеркнутых позиций: 1")
        self.assertContains(response, "Завершённых позиций: 1")
