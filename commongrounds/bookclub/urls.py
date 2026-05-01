from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
    path(
        "book/<int:pk>/",
        BookDetailView.as_view(),
        name="book_detail"),
]

app_name = "bookclub"
