"""Страницы списка покупок на шаблонах Django."""
from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_products, load_purchases, load_users

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
USERS_FILE = BASE_DIR / "data" / "users.json"
PURCHASES_FILE = BASE_DIR / "data" / "purchases.json"


def _load():
    """Загрузить позиции вместе с товарами и пользователями."""
    products = load_products(PRODUCTS_FILE)
    users = load_users(USERS_FILE)
    return load_purchases(PURCHASES_FILE, products, users)


def purchase_list(request):
    """Показать активные позиции списка."""
    purchases = []
    for purchase in _load():
        if purchase.is_cancelled:
            continue
        purchases.append({
            "id": purchase.id,
            "product_name": purchase.product.name,
            "quantity": purchase.product.quantity,
            "user_name": purchase.user.name,
            "purchase_date": purchase.purchase_date,
        })
    return render(
        request,
        "purchases/purchase_list.html",
        {"purchases": purchases},
    )


def purchase_detail(request, purchase_id):
    """Показать карточку позиции."""
    found = None
    for purchase in _load():
        if purchase.id == purchase_id:
            found = purchase
            break
    if found is None:
        raise Http404
    return render(
        request,
        "purchases/purchase_detail.html",
        {"purchase": found},
    )
