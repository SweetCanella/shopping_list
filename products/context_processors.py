"""Общие данные товаров для шаблонов."""
from .models import Product


def product_context(request):
    """Передать название приложения и число товаров."""
    return {
        "site_name": "Система формирования списка покупок",
        "products_count": Product.objects.count(),
    }
