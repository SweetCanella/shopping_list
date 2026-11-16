"""Маршруты товаров."""
from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("available/", views.available_products, name="available"),
    path("<slug:slug>/", views.product_detail, name="detail"),
]
