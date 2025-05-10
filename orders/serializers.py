# orders/serializers.py

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
    price_at_purchase = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    # Ya no especificamos source, usa por defecto 'items'
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items', 'total']
