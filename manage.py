#!/usr/bin/env python
"""Запуск административных команд Django."""
import os
import sys


def main():
    """Запустить команду Django."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "shoplist.settings",
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Проверьте, что виртуальное "
            "окружение создано и зависимости установлены."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
