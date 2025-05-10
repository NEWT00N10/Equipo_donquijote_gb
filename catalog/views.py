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
    Página de detalle de libro, con botón de 'Agregar al carrito' y 'Favorito'.
    """
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"
