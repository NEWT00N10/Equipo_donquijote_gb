from rest_framework import viewsets, permissions
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Permite a usuarios autenticados listar, crear y borrar sus favoritos.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo los favoritos del usuario autenticado
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario actual
        serializer.save(user=self.request.user)
