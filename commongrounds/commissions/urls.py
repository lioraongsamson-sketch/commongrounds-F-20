from django.urls import path
from .views import CommissionListView, CommissionDetailView


urlpatterns = [
    path('requests/', CommissionListView.as_view(), name='request_list'),
    path('request/<int:pk>',
         CommissionDetailView.as_view(), name='request_detail')
]

app_name = "commissions"
