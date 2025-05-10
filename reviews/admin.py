from django.contrib import admin
from reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("book", "user", "rating", "created_at")
    list_filter   = ("rating",)
    search_fields = ("book__title", "user__username", "comment")
    readonly_fields = ("created_at",)
