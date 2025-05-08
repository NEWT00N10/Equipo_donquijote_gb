from django.contrib import admin
from catalog.models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ("title", "author", "genre", "copies_available", "price")
    list_filter   = ("genre", "language", "publisher")
    search_fields = ("title", "author", "isbn_10", "isbn_13")
    readonly_fields = ("created_at", "updated_at")
