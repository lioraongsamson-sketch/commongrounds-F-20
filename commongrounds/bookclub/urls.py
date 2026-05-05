from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
    path(
        "book/<int:pk>/",
        BookDetailView.as_view(),
        name="book_detail"),
    path("book/add/", BookCreateView.as_view(), name="book_create")
]

app_name = "bookclub"
