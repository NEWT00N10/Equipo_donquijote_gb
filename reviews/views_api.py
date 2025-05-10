from rest_framework import viewsets, permissions
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Permite CRUD de reseñas: cada usuario solo puede modificar/suprimir las suyas.
    Cualquiera autenticado puede listar todas o las de un libro específico.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Si se proporciona ?book=<id>, filtra por ese libro.
        De lo contrario, retorna todas las reseñas.
        """
        qs = Review.objects.all()
        book_id = self.request.query_params.get("book")
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario de la solicitud
        serializer.save(user=self.request.user)
