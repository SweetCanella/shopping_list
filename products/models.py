"""Модель товара."""
from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Product(models.Model):
    """Товар списка покупок."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название товара",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
        help_text="Укажите, сколько единиц товара нужно купить.",
    )
    # В примере с помещениями порог равен 50. Для количества товара
    # большим считается запас от 5 единиц.
    is_large = models.GeneratedField(
        expression=Case(
            When(quantity__gte=5, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Большое количество",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )

    def save(self, *args, **kwargs):
        """Сформировать slug, если он ещё не задан."""
        if not self.slug:
            transliterated_name = unidecode(self.name)
            base_slug = slugify(transliterated_name) or "product"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Вернуть адрес подробной страницы товара."""
        return reverse(
            "products:detail",
            kwargs={"slug": self.slug},
        )

    def is_enough_for(self, needed):
        """Проверить, что количества товара достаточно."""
        return self.quantity >= needed

    def __str__(self):
        """Вернуть название товара."""
        return self.name

    class Meta:
        """Сортировка и названия модели."""

        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
