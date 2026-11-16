"""Проверки адреса товара и общего контекста шаблонов."""
from django.test import TestCase
from django.urls import reverse

from products.models import Product


class ProductSlugTests(TestCase):
    """Slug и подробная страница товара."""

    def test_new_product_gets_slug_and_page(self):
        """Новый товар открывается по сформированному адресу."""
        product = Product.objects.create(name="Молоко", quantity=2)
        product.refresh_from_db()
        self.assertEqual(product.slug, f"moloko-{product.pk}")
        self.assertFalse(product.is_large)
        response = self.client.get(product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Молоко")

    def test_large_quantity_is_calculated(self):
        """Признак большого количества считает база данных."""
        product = Product.objects.create(name="Яйца", quantity=10)
        product.refresh_from_db()
        self.assertTrue(product.is_large)

    def test_missing_slug_returns_404(self):
        """Несуществующий адрес товара возвращает 404."""
        response = self.client.get("/products/net-takogo-tovara/")
        self.assertEqual(response.status_code, 404)


class ProductContextTests(TestCase):
    """Контекстный процессор товаров."""

    def test_product_count_is_available_in_template(self):
        """Название и число товаров доступны в шаблоне."""
        Product.objects.create(name="Молоко", quantity=2)
        Product.objects.create(name="Хлеб", quantity=1)
        response = self.client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["site_name"],
            "Система формирования списка покупок",
        )
        self.assertEqual(response.context["products_count"], 2)
        self.assertContains(response, "Товары (2)")
