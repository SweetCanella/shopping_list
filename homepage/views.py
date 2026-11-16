"""Представление главной страницы."""
from pathlib import Path

from django.shortcuts import render

from storage import load_products, load_purchases, load_users

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
USERS_FILE = BASE_DIR / "data" / "users.json"
PURCHASES_FILE = BASE_DIR / "data" / "purchases.json"


def index(request):
    """Показать сводку по товарам и активным позициям."""
    products = load_products(PRODUCTS_FILE)
    users = load_users(USERS_FILE)
    purchases = load_purchases(PURCHASES_FILE, products, users)
    active = [
        purchase for purchase in purchases
        if not purchase.is_cancelled
    ]
    context = {
        "products_count": len(products),
        "purchases_count": len(active),
    }
    return render(request, "homepage/index.html", context)
