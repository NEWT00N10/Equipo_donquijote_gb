# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import CartItemViewSet, OrderViewSet
from .views import cart_view, checkout_view, OrderListView

# Router DRF para API REST
router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # 1) Página HTML de detalle de carrito
    path('', cart_view, name='cart-detail'),
    # 2) Página HTML de checkout
    path('checkout/', checkout_view, name='cart-checkout'),
    # 3) Lista de pedidos del usuario
    path('history/', OrderListView.as_view(), name='orders-list'),
    # 4) Endpoints REST bajo /cart/api/ y /orders/api/
    path('api/', include(router.urls)),
]
