from django.contrib import admin
from .models import Book, Genre, BookReview, Bookmark, Borrow


class BookInline(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre


class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview


class BookmarkAdmin(admin.ModelAdmin):
    model = Bookmark


class BorrowAdmin(admin.ModelAdmin):
    model = Borrow


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Borrow, BorrowAdmin)

# Register your models here.
