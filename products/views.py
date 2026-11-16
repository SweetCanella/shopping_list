"""Представления товаров."""
from datetime import datetime

from django.shortcuts import get_object_or_404, render

from products.models import Product
from purchases.models import Purchase


def product_list(request):
    """Показать товары с поиском, фильтром и сортировкой."""
    query = request.GET.get("q", "").strip()
    min_quantity = request.GET.get("min_quantity", "").strip()
    sort = request.GET.get("sort", "name")
    error = None

    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    if min_quantity:
        if min_quantity.isdigit():
            products = products.filter(
                quantity__gte=int(min_quantity),
            )
        else:
            error = "Укажите корректное количество."

    if sort == "quantity":
        products = products.order_by("-quantity", "name")
    else:
        sort = "name"
        products = products.order_by("name")

    context = {
        "products": products,
        "query": query,
        "min_quantity": min_quantity,
        "sort": sort,
        "error": error,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    """Показать карточку товара."""
    product = get_object_or_404(Product, pk=product_id)
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )


def available_products(request):
    """Найти товары, которых нет в активном списке на дату."""
    purchase_date = request.GET.get("date", "").strip()
    products_list = []
    error = None

    if purchase_date:
        try:
            selected_date = datetime.strptime(
                purchase_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            busy_ids = Purchase.objects.filter(
                purchase_date=selected_date,
                is_cancelled=False,
            ).values_list("product_id", flat=True)
            products_list = Product.objects.exclude(
                pk__in=busy_ids,
            ).order_by("name")

    context = {
        "products": products_list,
        "purchase_date": purchase_date,
        "error": error,
    }
    return render(request, "products/available.html", context)
