from django.contrib import admin
from orders.models import CartItem, Order, OrderItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "quantity")
    search_fields = ("user__username", "book__title")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price_at_purchase",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "total")
    search_fields = ("user__username",)
