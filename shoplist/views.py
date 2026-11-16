"""Обработчики проекта."""
from django.shortcuts import render


def page_not_found(request, exception):
    """Вернуть страницу 404."""
    return render(request, "404.html", status=404)
