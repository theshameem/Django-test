from django.views import generic
from django.db.models import Prefetch

from product.models import Product, Variant, ProductVariantPrice, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 2

    def get_queryset(self):
        qs = Product.objects.prefetch_related(
            "productvariantprice_set", "productvariant_set"
        ).order_by("created_at", "updated_at")
        title_filter = self.request.GET.get("title", "")
        date_filter = self.request.GET.get("date", "")
        price_from = self.request.GET.get("price_from", "")
        price_to = self.request.GET.get("price_to", "")
        if title_filter != "" and title_filter is not None:
            qs = qs.filter(
                title__icontains=title_filter,
            )
        if date_filter != "" and date_filter is not None:
            qs = qs.filter(
                created_at__gte=date_filter,
            )
        if price_from != "" and price_from is not None:
            qs = qs.filter(productvariantprice__price__range=(
                price_from, price_to))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["title_filter"] = self.request.GET.get("title", "")
        context["date_filter"] = self.request.GET.get("date", "")
        context["price_from"] = self.request.GET.get("price_from", "")
        context["price_to"] = self.request.GET.get("price_to", "")
        context["variants"] = list(
            Variant.objects.filter(active=True).prefetch_related(
                "productvariant_set",
            )
        )

        return context
