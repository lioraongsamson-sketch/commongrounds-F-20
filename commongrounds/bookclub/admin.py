from django.contrib import admin
from .models import Book, Genre


class BookInline(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)

# Register your models here.
