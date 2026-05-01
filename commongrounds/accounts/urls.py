from django.urls import path 
from .views import ProfileUpdateView 

urlpatterns = [ 
    path('<str:display_name>/update', ProfileUpdateView.as_view()), 
]
app_name = 'accounts'