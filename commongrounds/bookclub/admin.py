from django.contrib import admin
from .models import Book, Genre


class BookInline(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [
        BookInline,
    ]


admin.site.register(Genre, GenreAdmin)

# Register your models here.
