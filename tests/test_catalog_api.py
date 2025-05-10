import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from catalog.models import Book

@pytest.mark.django_db
def test_book_filters_and_ordering():
    # Crear datos de prueba
    Book.objects.create(title="A", author="X", genre="FIC", price=100, book_type="PHYS")
    Book.objects.create(title="B", author="Y", genre="SCI", price=50,  book_type="EBOOK")
    client = APIClient()

    # Filtrar por genre=FIC
    url = reverse("book-list") + "?genre=FIC"
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()["results"]
    assert len(data) == 1 and data[0]["genre"] == "FIC"

    # Filtrar por tipo EBOOK
    url = reverse("book-list") + "?book_type=EBOOK"
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()["results"]
    assert len(data) == 1 and data[0]["book_type"] == "EBOOK"

    # Ordenar por precio ascendente
    url = reverse("book-list") + "?ordering=price"
    response = client.get(url)
    prices = [b["price"] for b in response.json()["results"]]
    assert prices == sorted(prices)
