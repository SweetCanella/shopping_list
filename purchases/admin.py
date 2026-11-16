"""Административный интерфейс позиций списка покупок."""
from django.contrib import admin
from django.contrib import messages

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Список позиций, поиск, фильтры и массовые действия."""

    list_display = (
        "id",
        "product",
        "user",
        "product_quantity",
        "purchase_date",
        "status",
    )
    list_display_links = ("id",)
    search_fields = ("product__name", "user__name")
    list_filter = ("purchase_date", "status")
    ordering = ("-purchase_date",)
    list_per_page = 20
    readonly_fields = ("id",)
    list_select_related = ("product", "user")
    date_hierarchy = "purchase_date"
    autocomplete_fields = ("product", "user")
    actions = (
        "cancel_purchases",
        "restore_purchases",
        "delete_selected",
    )

    @admin.display(
        description="Количество",
        ordering="product__quantity",
    )
    def product_quantity(self, obj):
        """Показать количество связанного товара."""
        return obj.product.quantity

    @admin.action(description="Вычеркнуть выбранные позиции")
    def cancel_purchases(self, request, queryset):
        """Вычеркнуть отмеченные позиции методом модели."""
        count = 0
        for purchase in queryset:
            purchase.cancel()
            count += 1
        self.message_user(
            request,
            f"Вычеркнуто позиций: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в активные")
    def restore_purchases(self, request, queryset):
        """Вернуть отмеченные позиции в активное состояние."""
        updated = queryset.update(status=Purchase.Status.ACTIVE)
        self.message_user(
            request,
            f"Возвращено позиций: {updated}.",
            messages.SUCCESS,
        )
