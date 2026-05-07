from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView


urlpatterns = [
    path('requests/', CommissionListView.as_view(), name='request_list'),
    path('request/<int:pk>',
         CommissionDetailView.as_view(), name='request_detail'),
    path('request/add', CommissionCreateView.as_view(), name='request_create'),
    path('request/<int:pk>/edit', CommissionUpdateView.as_view(), name='request_update'),

]

app_name = "commissions"
