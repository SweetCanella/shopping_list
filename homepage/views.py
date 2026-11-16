"""Представление главной страницы."""
from django.db.models import Count
from django.shortcuts import render

from products.models import Product
from purchases.models import Purchase


def index(request):
    """Показать сводку по товарам и активным позициям."""
    summary = Purchase.objects.filter(is_cancelled=False).aggregate(
        purchases_count=Count("id"),
    )
    context = {
        "products_count": Product.objects.count(),
        "purchases_count": summary["purchases_count"],
    }
    return render(request, "homepage/index.html", context)
