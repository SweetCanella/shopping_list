"""Административный интерфейс товаров."""
from django.contrib import admin
from django.db.models import Count, Q

from purchases.models import Purchase

from .models import Product


class PurchaseInline(admin.TabularInline):
    """Связанные позиции на странице товара."""

    model = Purchase
    fields = ("user", "purchase_date", "is_cancelled")
    extra = 0
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Список товаров, поиск и связанные позиции."""

    list_display = (
        "id",
        "name",
        "quantity",
        "active_purchases_count",
    )
    list_display_links = ("name",)
    list_editable = ("quantity",)
    search_fields = ("name",)
    list_filter = ("quantity",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (PurchaseInline,)

    def get_queryset(self, request):
        """Посчитать активные позиции одним запросом."""
        queryset = super().get_queryset(request)
        return queryset.annotate(
            active_purchases=Count(
                "purchases",
                filter=Q(purchases__is_cancelled=False),
            ),
        )

    @admin.display(
        description="Активных позиций",
        ordering="active_purchases",
    )
    def active_purchases_count(self, obj):
        """Вернуть число активных позиций товара."""
        return obj.active_purchases
