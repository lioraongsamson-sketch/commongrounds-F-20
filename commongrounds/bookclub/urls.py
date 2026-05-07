from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookBorrowView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/add/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/edit/", BookUpdateView.as_view(), name="book_edit"),
    path("book/<int:pk>/borrow/", BookBorrowView.as_view(), name="book_borrow"),
]

app_name = "bookclub"
