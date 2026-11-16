"""Корневая маршрутизация проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("products/", include("products.urls")),
    path("purchases/", include("purchases.urls")),
]

handler404 = "shoplist.views.page_not_found"
