"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views_api import BookViewSet
from circulation.views_api import LoanViewSet, ReservationViewSet
from favorites.views_api import FavoriteViewSet
from reviews.views_api import ReviewViewSet
from orders.views_api import CartItemViewSet, OrderViewSet

from catalog.views import BookListView, BookDetailView
from orders.views import cart_view, checkout_view
from orders.views import profile_view



router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"cart", CartItemViewSet, basename="cartitem")
router.register(r"orders", OrderViewSet, basename="order")




urlpatterns = [
    # Frontend
    path("", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("cart/", cart_view, name="cart-view"),
    path("checkout/", checkout_view, name="cart-checkout"),
    # Admin
    path("admin/", admin.site.urls),
    # API
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # Dashboard de usuario
    path("profile/", profile_view, name="profile"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


