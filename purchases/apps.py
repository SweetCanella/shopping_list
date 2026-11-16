from django.apps import AppConfig


class PurchasesConfig(AppConfig):
    """Приложение позиций списка покупок."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "purchases"
    verbose_name = "Список покупок"
