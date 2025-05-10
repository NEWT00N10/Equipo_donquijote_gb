from django.contrib import admin
from favorites.models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display  = ("user", "book", "created_at")
    list_filter   = ("created_at",)
    search_fields = ("user__username", "book__title")
