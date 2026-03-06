from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
    path('bookclub/books/', BookListView.as_view(), name='book_list'),
    path('bookclub/book/<int:pk>/', BookDetailView.as_view(), name='book_detail')
]

app_name = "bookclub"