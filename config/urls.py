from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

# API ViewSets
from catalog.views_api     import BookViewSet
from circulation.views_api import LoanViewSet, ReservationViewSet
from favorites.views_api   import FavoriteViewSet
from reviews.views_api     import ReviewViewSet
from orders.views_api      import CartItemViewSet, OrderViewSet

# Frontend views
from catalog.views import home_view, BookListView, BookDetailView
from orders.views  import cart_view, checkout_view, OrderListView, profile_view

# Configuramos el router DRF
router = DefaultRouter()
router.register(r'books',        BookViewSet,        basename='book')
router.register(r'loans',        LoanViewSet,        basename='loan')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'favorites',    FavoriteViewSet,    basename='favorite')
router.register(r'reviews',      ReviewViewSet,      basename='review')
router.register(r'cart',         CartItemViewSet,    basename='cart')
router.register(r'orders',       OrderViewSet,       basename='order')

urlpatterns = [
    # Home y catálogo
    path("",                    home_view,               name='home'),
    path("books/",              BookListView.as_view(),   name='book-list'),
    path("books/<int:pk>/",     BookDetailView.as_view(), name='book-detail'),

    # Carrito y checkout
    path("cart/",               cart_view,                name='cart-view'),
    path("checkout/",           checkout_view,            name='cart-checkout'),

    # Historial de pedidos y perfil
    path("orders/history/",     OrderListView.as_view(),  name='orders-list'),
    path("profile/",            profile_view,             name='profile'),

    # Favoritos (HTML + API)
    path("favorites/",          include("favorites.urls")),

    # Administración y auth
    path("admin/",              admin.site.urls),
    path("accounts/",           include("django.contrib.auth.urls")),

    # API REST global
    path("api/",                include(router.urls)),
    path("api-auth/",           include("rest_framework.urls")),
]

# Servir estáticos y media en DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,  document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)
