from django.urls import path 
from .views import ProfileUpdateView 

urlpatterns = [ 
    path('<pk>/update', ProfileUpdateView.as_view()), 
]
app_name = 'accounts'