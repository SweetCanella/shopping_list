"""Страницы списка покупок читают данные из SQLite."""
from datetime import date
from types import SimpleNamespace

from django.http import Http404
from django.shortcuts import render

from db.database import get_connection


def purchase_list(request):
    """Показать активные позиции списка."""
    connection = get_connection()
    try:
        rows = connection.execute(
            """
            SELECT
                purchases.id,
                purchases.purchase_date,
                products.name AS product_name,
                products.quantity,
                users.name AS user_name
            FROM purchases
            JOIN products ON purchases.product_id = products.id
            JOIN users ON purchases.user_id = users.id
            WHERE purchases.is_cancelled = 0
            ORDER BY purchases.purchase_date, purchases.id
            """
        ).fetchall()
    finally:
        connection.close()
    purchases = []
    for row in rows:
        purchases.append({
            "id": row["id"],
            "purchase_date": date.fromisoformat(row["purchase_date"]),
            "product_name": row["product_name"],
            "quantity": row["quantity"],
            "user_name": row["user_name"],
        })
    return render(
        request,
        "purchases/purchase_list.html",
        {"purchases": purchases},
    )


def purchase_detail(request, purchase_id):
    """Показать карточку позиции."""
    connection = get_connection()
    try:
        row = connection.execute(
            """
            SELECT
                purchases.id,
                purchases.purchase_date,
                purchases.is_cancelled,
                products.name AS product_name,
                products.quantity,
                users.name AS user_name,
                users.email
            FROM purchases
            JOIN products ON purchases.product_id = products.id
            JOIN users ON purchases.user_id = users.id
            WHERE purchases.id = ?
            """,
            (purchase_id,),
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        raise Http404
    purchase = SimpleNamespace(
        id=row["id"],
        purchase_date=date.fromisoformat(row["purchase_date"]),
        is_cancelled=bool(row["is_cancelled"]),
        product=SimpleNamespace(
            name=row["product_name"],
            quantity=row["quantity"],
        ),
        user=SimpleNamespace(
            name=row["user_name"],
            email=row["email"],
        ),
    )
    return render(
        request,
        "purchases/purchase_detail.html",
        {"purchase": purchase},
    )


def statistics(request):
    """Показать число активных позиций по товарам."""
    connection = get_connection()
    try:
        statistics_data = connection.execute(
            """
            SELECT
                products.name AS product_name,
                COUNT(purchases.id) AS purchases_count
            FROM products
            LEFT JOIN purchases
                ON products.id = purchases.product_id
                AND purchases.is_cancelled = 0
            GROUP BY products.id, products.name
            ORDER BY purchases_count DESC, products.name
            """
        ).fetchall()
        popular = connection.execute(
            """
            SELECT
                products.name AS name,
                COUNT(purchases.id) AS purchases_count
            FROM products
            JOIN purchases ON products.id = purchases.product_id
            WHERE purchases.is_cancelled = 0
            GROUP BY products.id, products.name
            HAVING COUNT(purchases.id) > 1
            ORDER BY purchases_count DESC, products.name
            """
        ).fetchall()
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
        "statistics": statistics_data,
        "popular": popular,
        "purchases_count": purchases_count,
    }
    return render(request, "purchases/statistics.html", context)
