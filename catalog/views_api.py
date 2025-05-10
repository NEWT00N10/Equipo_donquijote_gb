from rest_framework import viewsets, permissions
from catalog.models import Book
from catalog.serializers import BookSerializer
from api.permissions import IsLibrarianOrAdmin

class BookViewSet(viewsets.ModelViewSet):        # ← era ReadOnly
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = [permissions.AllowAny]  # solo lectura pública
