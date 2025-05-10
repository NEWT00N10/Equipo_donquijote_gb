from rest_framework import serializers
from orders.models import CartItem, Order, OrderItem
from catalog.serializers import BookSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__("catalog").models.Book.objects.all(),
        source="book",
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "book", "book_id", "quantity")

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("book", "quantity", "price_at_purchase")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "total", "items")
        read_only_fields = ("id", "user", "created_at", "total", "items")

