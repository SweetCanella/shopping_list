"""Обработчики проекта."""
from django.http import HttpResponse

from homepage.views import page


def page_not_found(request, exception):
    """Вернуть страницу 404."""
    html = page(
        "Страница не найдена",
        "<h1>Страница не найдена</h1>",
    )
    return HttpResponse(html, status=404)
