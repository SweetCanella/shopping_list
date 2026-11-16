"""Маршруты списка покупок."""
from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchase_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:purchase_id>/", views.purchase_detail, name="detail"),
]
