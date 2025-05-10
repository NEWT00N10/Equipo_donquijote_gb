# favorites/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import FavoriteViewSet
from .views import FavoritesListView

# 1) Configuramos el router para la API REST de favoritos
router = DefaultRouter()
router.register(r'', FavoriteViewSet, basename='favorite')

urlpatterns = [
    # Ruta HTML para la página de favoritos
    path('', FavoritesListView.as_view(), name='favorites-list'),

    # Todas las rutas de la API quedan bajo /favorites/api/
    path('api/', include(router.urls)),
]
