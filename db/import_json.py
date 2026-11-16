"""Перенос данных из JSON-файлов в SQLite."""
import json
from pathlib import Path

from database import get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def load_json(filename):
    """Прочитать список записей из JSON-файла."""
    with (DATA_DIR / filename).open(encoding="utf-8") as source:
        return json.load(source)


def main():
    """Создать таблицы и заполнить их данными из JSON."""
    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    connection = get_connection()
    try:
        connection.executescript(schema)
        connection.execute("DELETE FROM purchases")
        connection.execute("DELETE FROM users")
        connection.execute("DELETE FROM products")
        for row in load_json("products.json"):
            connection.execute(
                """
                INSERT INTO products (id, name, quantity)
                VALUES (?, ?, ?)
                """,
                (row["id"], row["name"], row["quantity"]),
            )
        for row in load_json("users.json"):
            connection.execute(
                """
                INSERT INTO users (id, name, email)
                VALUES (?, ?, ?)
                """,
                (row["id"], row["name"], row["email"]),
            )
        for row in load_json("purchases.json"):
            connection.execute(
                """
                INSERT INTO purchases (
                    id,
                    product_id,
                    user_id,
                    purchase_date,
                    is_cancelled
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    row["product_id"],
                    row["user_id"],
                    row["purchase_date"],
                    int(row["is_cancelled"]),
                ),
            )
        connection.commit()
    finally:
        connection.close()
    print("Импорт JSON в SQLite завершён.")


if __name__ == "__main__":
    main()
