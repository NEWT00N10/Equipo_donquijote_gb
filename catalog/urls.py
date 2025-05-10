from django.urls import path
from .views import home_view, BookListView, BookDetailView

app_name = "catalog"

urlpatterns = [
    # Home
    path("", home_view, name="home"),

    # Catálogo: listado y detalle
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
]
