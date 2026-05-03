from django.urls import path
from .views import ProductDetailView, ProductListView, ProductCreateView
from .views import ProductUpdateView, CartView, TransactionListView

app_name = 'merchstore'

urlpatterns =[
    path('items', ProductListView.as_view(), name="product_list"),
    path('item/add', ProductCreateView.as_view(), name="product_create"),
    path('item/<int:pk>',
         ProductDetailView.as_view(), name="product_detail"),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name="product_update"),
    path('cart', CartView.as_view(), name="cart_view"),
    path('transactions', TransactionListView.as_view(), name="transaction_list")
]
