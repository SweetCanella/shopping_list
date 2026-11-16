"""Страницы товаров на шаблонах Django."""
from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_products

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"


def product_list(request):
    """Показать товары с поиском, фильтром и сортировкой."""
    query = request.GET.get("q", "").strip()
    min_quantity = request.GET.get("min_quantity", "").strip()
    sort = request.GET.get("sort", "name")
    error = None
    products = list(load_products(PRODUCTS_FILE).values())
    if query:
        prepared = query.casefold()
        products = [
            product for product in products
            if prepared in product.name.casefold()
        ]
    if min_quantity:
        if min_quantity.isdigit():
            border = int(min_quantity)
            products = [
                product for product in products
                if product.quantity >= border
            ]
        else:
            error = "Укажите корректное количество."
    if sort == "quantity":
        products.sort(
            key=lambda product: (-product.quantity, product.name),
        )
    else:
        sort = "name"
        products.sort(key=lambda product: product.name)
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
    product = load_products(PRODUCTS_FILE).get(product_id)
    if product is None:
        raise Http404
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )
