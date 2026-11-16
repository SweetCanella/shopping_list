from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Приложение товаров."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
    verbose_name = "Товары"
