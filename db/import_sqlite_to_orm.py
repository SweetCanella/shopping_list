"""Перенос данных из базы ПР7 в базу Django ORM."""
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.core.management.color import no_style
from django.db import connection as django_connection
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
SOURCE_DB = BASE_DIR / "data" / "shoplist.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoplist.settings")
django.setup()

from products.models import Product  # noqa: E402
from purchases.models import Purchase  # noqa: E402
from users.models import User  # noqa: E402


def main():
    """Перенести товары, пользователей и позиции списка."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}"
        )
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        products = connection.execute(
            """
            SELECT id, name, quantity
            FROM products
            ORDER BY id
            """
        ).fetchall()
        users = connection.execute(
            """
            SELECT id, name, email
            FROM users
            ORDER BY id
            """
        ).fetchall()
        purchases = connection.execute(
            """
            SELECT
                id,
                product_id,
                user_id,
                purchase_date,
                is_cancelled
            FROM purchases
            ORDER BY id
            """
        ).fetchall()
        with transaction.atomic():
            for row in products:
                Product.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "quantity": row["quantity"],
                    },
                )
            for row in users:
                User.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "email": row["email"],
                    },
                )
            for row in purchases:
                Purchase.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "product_id": row["product_id"],
                        "user_id": row["user_id"],
                        "purchase_date": date.fromisoformat(
                            row["purchase_date"]
                        ),
                        "is_cancelled": bool(row["is_cancelled"]),
                    },
                )
            sequence_sql = django_connection.ops.sequence_reset_sql(
                no_style(),
                [Product, User, Purchase],
            )
            with django_connection.cursor() as cursor:
                for statement in sequence_sql:
                    cursor.execute(statement)
    print("Перенос данных завершён.")
    print(f"Товаров: {Product.objects.count()}")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Позиций: {Purchase.objects.count()}")


if __name__ == "__main__":
    main()
