"""Сборка HTML-страниц и главная страница."""
from pathlib import Path

from django.http import HttpResponse

from storage import load_products, load_purchases, load_users

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
USERS_FILE = BASE_DIR / "data" / "users.json"
PURCHASES_FILE = BASE_DIR / "data" / "purchases.json"


def page(title, content):
    """Собрать HTML-страницу с Bootstrap."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    parts = [
        "<!DOCTYPE html>",
        "<html lang=\"ru\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        f"<title>{title}</title>",
        f"<link rel=\"stylesheet\" href=\"{bootstrap}\">",
        "<style>body { background-color: #f8f9fa; }</style>",
        "</head>",
        "<body>",
        "<nav class=\"navbar bg-body-tertiary mb-4\">",
        "<div class=\"container\">",
        "<a class=\"navbar-brand\" href=\"/\">Список покупок</a>",
        "<a class=\"nav-link d-inline\" href=\"/products/\">",
        "Товары</a>",
        "<a class=\"nav-link d-inline\" href=\"/purchases/\">",
        "Список покупок</a>",
        "</div>",
        "</nav>",
        "<main class=\"container pb-5\">",
        content,
        "</main>",
        "</body>",
        "</html>",
    ]
    return "\n".join(parts)


def index(request):
    """Показать сводку по товарам и позициям."""
    products = load_products(PRODUCTS_FILE)
    users = load_users(USERS_FILE)
    purchases = load_purchases(
        PURCHASES_FILE,
        products,
        users,
    )
    active = [
        purchase for purchase in purchases
        if not purchase.is_cancelled
    ]
    content = (
        "<h1>Система формирования списка покупок</h1>"
        f"<p>Товаров: {len(products)}</p>"
        f"<p>Активных позиций: {len(active)}</p>"
    )
    return HttpResponse(page("Главная", content))
