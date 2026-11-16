from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Приложение пользователей предметной области."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"
