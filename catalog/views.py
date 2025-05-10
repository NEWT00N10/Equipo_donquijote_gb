from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from catalog.models import Book
from catalog.filters import BookFilter

class BookListView(FilterView, ListView):
    """
    Listado público de libros con filtros y paginación.
    """
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    filterset_class = BookFilter
    paginate_by = 20

class BookDetailView(DetailView):
    """
    Página de detalle de libro, con botones de 'Agregar al carrito' y 'Favorito'.
    """
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"

def home_view(request):
    """
    Vista de inicio con carousel de banners.
    Construye las URLs con reverse() para evitar plantillas en el contexto.
    """
    banners = [
        {
            "title": "Bienvenido a Don Quijote GB",
            "subtitle": "Tu librería favorita en línea",
            "link": reverse("book-list"),
            "button_text": "Ver catálogo"
        },
        {
            "title": "Promociones Exclusivas",
            "subtitle": "Descuentos hasta 50% en bestsellers",
            "link": "#",
            "button_text": "Descúbrelo"
        },
        {
            "title": "Novedades 2025",
            "subtitle": "Lo último en literatura moderna",
            "link": "#",
            "button_text": "Explorar"
        },
    ]
    return render(request, "home.html", {"banners": banners})
