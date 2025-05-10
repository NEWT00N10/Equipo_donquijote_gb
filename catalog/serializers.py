from rest_framework import serializers
from catalog.models import Book

class BookSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False  # <-- devuelve número, no string
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'book_type', 'price', 'cover']
