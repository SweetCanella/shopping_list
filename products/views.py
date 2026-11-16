"""Страницы товаров."""
from pathlib import Path

from django.http import HttpResponse

from homepage.views import page
from storage import load_products

BASE_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"


def product_list(request):
    """Показать товары из JSON."""
    products = load_products(PRODUCTS_FILE)
    blocks = ["<h1>Товары</h1>"]
    for product in products.values():
        blocks.append(
            "<article class=\"card mb-3\"><div class=\"card-body\">"
            f"<h2 class=\"h5\">{product.name}</h2>"
            f"<p>Количество: {product.quantity}</p>"
            f"<a href=\"/products/{product.id}/\">Подробнее</a>"
            "</div></article>"
        )
    if not products:
        blocks.append("<p>Товары отсутствуют.</p>")
    return HttpResponse(page("Товары", "\n".join(blocks)))


def product_detail(request, product_id):
    """Показать карточку товара."""
    products = load_products(PRODUCTS_FILE)
    product = products.get(product_id)
    if product is None:
        html = page(
            "Товар не найден",
            "<h1>Товар не найден</h1>",
        )
        return HttpResponse(html, status=404)
    content = (
        f"<h1>{product.name}</h1>"
        f"<p>Количество: {product.quantity}</p>"
        "<a href=\"/products/\">К списку товаров</a>"
    )
    return HttpResponse(page(product.name, content))
