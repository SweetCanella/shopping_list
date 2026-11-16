"""Страницы списка покупок."""
from pathlib import Path

from django.http import HttpResponse

from homepage.views import page
from storage import load_products, load_purchases, load_users

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
USERS_FILE = BASE_DIR / "data" / "users.json"
PURCHASES_FILE = BASE_DIR / "data" / "purchases.json"


def _load():
    """Загрузить объекты предметной области."""
    products = load_products(PRODUCTS_FILE)
    users = load_users(USERS_FILE)
    purchases = load_purchases(PURCHASES_FILE, products, users)
    return purchases


def purchase_list(request):
    """Показать активные позиции списка."""
    blocks = ["<h1>Список покупок</h1>"]
    active = [
        purchase for purchase in _load()
        if not purchase.is_cancelled
    ]
    for purchase in active:
        blocks.append(
            "<article class=\"card mb-3\"><div class=\"card-body\">"
            f"<h2 class=\"h5\">{purchase.product.name}</h2>"
            f"<p>Пользователь: {purchase.user.name}</p>"
            f"<p>Дата: {purchase.purchase_date:%d.%m.%Y}</p>"
            f"<a href=\"/purchases/{purchase.id}/\">Подробнее</a>"
            "</div></article>"
        )
    if not active:
        blocks.append("<p>Активные позиции не найдены.</p>")
    return HttpResponse(page("Список покупок", "\n".join(blocks)))


def purchase_detail(request, purchase_id):
    """Показать карточку позиции."""
    found = None
    for purchase in _load():
        if purchase.id == purchase_id:
            found = purchase
            break
    if found is None:
        html = page(
            "Позиция не найдена",
            "<h1>Позиция не найдена</h1>",
        )
        return HttpResponse(html, status=404)
    content = (
        f"<h1>Позиция №{found.id}</h1>"
        f"<p>Товар: {found.product.name}</p>"
        f"<p>Количество: {found.product.quantity}</p>"
        f"<p>Пользователь: {found.user.name}</p>"
        f"<p>Дата: {found.purchase_date:%d.%m.%Y}</p>"
        f"<p>Статус: {found.status}</p>"
        "<a href=\"/purchases/\">К списку покупок</a>"
    )
    return HttpResponse(page(f"Позиция №{found.id}", content))
