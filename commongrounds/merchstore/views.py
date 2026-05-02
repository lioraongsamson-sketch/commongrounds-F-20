from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product, Transaction
from .forms import TransactionForm
from django.shortcuts import redirect
from django.urls import reverse


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products_all"

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
            context['products_user'] = None
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_object_name(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        product = self.get_object()

        if not request.user.is_authenticated:
            login_url = reverse('login')
            return redirect(f"{login_url}?next={request.path}")

        if request.user == product.owner:
            return redirect('product_detail', pk=product.pk)
        
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)

            if product.stock >= transaction.amount and product.stock > 0:
                product.stock -= transaction.amount
                product.save()

                transaction.product = product
                transaction.buyer = request.user.profile
                transaction.status = 'On cart'
                transaction.save()

                return redirect('cart_view')
            else:
                return redirect('product_detail', pk=product.pk)
        return self.get(request, *args, **kwargs)