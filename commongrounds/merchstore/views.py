from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = Product.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.exclude(owner=self.request.user)
        return queryset
    
    def get_context_object_name(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.reqest.user.is_authenticated:
            context['products_user'] = Product.object.filter(owner=self.request.user)
        else:
            context['product_user'] = None
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
