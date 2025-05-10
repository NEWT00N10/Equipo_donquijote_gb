import django_filters as filters
from catalog.models import Book

class BookFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Book
        fields = {
            "genre": ["exact"],
            "book_type": ["exact"],
        }
