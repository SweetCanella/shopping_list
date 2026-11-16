"""Административный интерфейс пользователей предметной области."""
from django.contrib import admin

from purchases.models import Purchase

from .models import User


class PurchaseInline(admin.TabularInline):
    """Связанные позиции на странице пользователя."""

    model = Purchase
    fields = ("product", "purchase_date", "status")
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Список пользователей предметной области."""

    list_display = ("id", "name", "email")
    list_display_links = ("name",)
    search_fields = ("name", "email")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (PurchaseInline,)
