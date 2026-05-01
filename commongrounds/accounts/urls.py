from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    path('<str:username>/', ProfileUpdateView.as_view(), name="profile_update"),
]
app_name = 'accounts'
