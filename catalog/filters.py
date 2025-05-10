from django import forms
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    genre = django_filters.ChoiceFilter(
        field_name='genre',
        lookup_expr='exact',
        choices=Book.GENRE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    book_type = django_filters.ChoiceFilter(
        field_name='book_type',
        lookup_expr='exact',
        choices=Book.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Mín'})
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Máx'})
    )

    class Meta:
        model = Book
        fields = ['genre', 'book_type', 'min_price', 'max_price']
