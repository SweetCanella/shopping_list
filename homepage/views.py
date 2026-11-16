"""Главная страница читает сводку из SQLite."""
from django.shortcuts import render

from db.database import get_connection


def index(request):
    """Показать число товаров и активных позиций."""
    connection = get_connection()
    try:
        products_count = connection.execute(
            "SELECT COUNT(*) AS total FROM products"
        ).fetchone()["total"]
        purchases_count = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM purchases
            WHERE is_cancelled = 0
            """
        ).fetchone()["total"]
    finally:
        connection.close()
    context = {
        "products_count": products_count,
        "purchases_count": purchases_count,
    }
    return render(request, "homepage/index.html", context)
