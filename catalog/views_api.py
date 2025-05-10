from rest_framework import filters
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Book
from catalog.serializers import BookSerializer
from catalog.filters import BookFilter




class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listado público con filtros avanzados.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,          # ← añade SearchFilter
    ]
    filterset_fields = ['genre', 'book_type']
    filterset_class = BookFilter
    ordering_fields   = ['price', 'title', 'author']
    search_fields = ["title", "author", "isbn_10", "isbn_13"]


