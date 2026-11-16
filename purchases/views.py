"""Представления списка покупок."""
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render

from products.models import Product
from purchases.models import Purchase
from users.models import User


def purchase_list(request):
    """Показать активные позиции с фильтрами, сортировкой и страницами."""
    purchase_date = request.GET.get("date", "").strip()
    product_id = request.GET.get("product", "").strip()
    user_id = request.GET.get("user", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    purchases_data = Purchase.objects.filter(is_cancelled=False)

    if purchase_date:
        try:
            selected_date = datetime.strptime(
                purchase_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            purchases_data = purchases_data.filter(
                purchase_date=selected_date,
            )

    if product_id.isdigit():
        purchases_data = purchases_data.filter(
            product_id=int(product_id),
        )
    if user_id.isdigit():
        purchases_data = purchases_data.filter(user_id=int(user_id))
    if query:
        purchases_data = purchases_data.filter(
            Q(product__name__icontains=query)
            | Q(user__name__icontains=query)
        )

    purchases_data = purchases_data.annotate(
        product_name=F("product__name"),
        quantity=F("product__quantity"),
        user_name=F("user__name"),
    )
    sort_fields = {
        "date": "purchase_date",
        "product": "product__name",
        "user": "user__name",
    }
    sort_field = sort_fields.get(sort, "purchase_date")
    if sort not in sort_fields:
        sort = "date"
    purchases_data = purchases_data.order_by(sort_field, "id")
    purchases_data = purchases_data.values(
        "id",
        "purchase_date",
        "product_name",
        "quantity",
        "user_name",
    )

    paginator = Paginator(purchases_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "purchases": page_obj,
        "page_obj": page_obj,
        "purchase_date": purchase_date,
        "selected_product": product_id,
        "selected_user": user_id,
        "query": query,
        "sort": sort,
        "products": Product.objects.order_by("name"),
        "users": User.objects.order_by("name"),
        "error": error,
    }
    return render(request, "purchases/purchase_list.html", context)


def purchase_detail(request, purchase_id):
    """Показать карточку позиции вместе со связанными объектами."""
    purchase = get_object_or_404(
        Purchase.objects.select_related("product", "user"),
        pk=purchase_id,
    )
    return render(
        request,
        "purchases/purchase_detail.html",
        {"purchase": purchase},
    )


def statistics(request):
    """Показать число активных позиций по каждому товару."""
    statistics_data = (
        Product.objects.annotate(
            purchases_count=Count(
                "purchases",
                filter=Q(purchases__is_cancelled=False),
            ),
            product_name=F("name"),
        )
        .values("product_name", "purchases_count")
        .order_by("-purchases_count", "product_name")
    )
    popular = (
        Product.objects.annotate(
            purchases_count=Count(
                "purchases",
                filter=Q(purchases__is_cancelled=False),
            ),
        )
        .filter(purchases_count__gt=1)
        .order_by("-purchases_count", "name")
    )
    summary = Purchase.objects.filter(is_cancelled=False).aggregate(
        purchases_count=Count("id"),
    )
    context = {
        "statistics": statistics_data,
        "popular": popular,
        "purchases_count": summary["purchases_count"],
    }
    return render(request, "purchases/statistics.html", context)
