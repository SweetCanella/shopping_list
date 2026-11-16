"""Страницы товаров читают данные из SQLite."""
from datetime import datetime

from django.http import Http404
from django.shortcuts import render

from db.database import get_connection


def product_list(request):
    """Показать товары с поиском, фильтром и сортировкой."""
    query = request.GET.get("q", "").strip()
    min_quantity = request.GET.get("min_quantity", "").strip()
    sort = request.GET.get("sort", "name")
    error = None
    clauses = []
    params = []
    if query:
        clauses.append("name LIKE ?")
        params.append(f"%{query}%")
    if min_quantity:
        if min_quantity.isdigit():
            clauses.append("quantity >= ?")
            params.append(int(min_quantity))
        else:
            error = "Укажите корректное количество."
    where = ""
    if clauses:
        where = "WHERE " + " AND ".join(clauses)
    if sort == "quantity":
        order = "quantity DESC, name"
    else:
        sort = "name"
        order = "name"
    connection = get_connection()
    try:
        products = connection.execute(
            f"""
            SELECT id, name, quantity
            FROM products
            {where}
            ORDER BY {order}
            """,
            params,
        ).fetchall()
    finally:
        connection.close()
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
    connection = get_connection()
    try:
        product = connection.execute(
            """
            SELECT id, name, quantity
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()
    finally:
        connection.close()
    if product is None:
        raise Http404
    return render(
        request,
        "products/product_detail.html",
        {"product": product},
    )


def available_products(request):
    """Найти товары без активной позиции на выбранную дату."""
    purchase_date = request.GET.get("date", "").strip()
    products = []
    error = None
    if purchase_date:
        try:
            datetime.strptime(purchase_date, "%Y-%m-%d")
        except ValueError:
            error = "Укажите корректную дату."
        else:
            connection = get_connection()
            try:
                products = connection.execute(
                    """
                    SELECT id, name, quantity
                    FROM products
                    WHERE id NOT IN (
                        SELECT product_id
                        FROM purchases
                        WHERE purchase_date = ?
                            AND is_cancelled = 0
                    )
                    ORDER BY name
                    """,
                    (purchase_date,),
                ).fetchall()
            finally:
                connection.close()
    context = {
        "products": products,
        "purchase_date": purchase_date,
        "error": error,
    }
    return render(request, "products/available.html", context)
