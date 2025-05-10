import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from catalog.models import Book
from orders.models import CartItem, Order

User = get_user_model()

@pytest.mark.django_db
def test_cart_and_order_flow():
    user = User.objects.create_user(username="u2", password="pass2")
    # Libro con stock
    book = Book.objects.create(title="Y", author="B", genre="FIC", price=20, copies_available=5)

    client = APIClient()
    client.force_authenticate(user)

    # Añadir al carrito
    resp = client.post("/api/cart/", {"book_id": book.id, "quantity": 2}, format="json")
    assert resp.status_code == 201
    assert CartItem.objects.filter(user=user).count() == 1

    # Crear pedido
    resp = client.post("/api/orders/")
    assert resp.status_code == 201
    data = resp.json()
    assert data["total"] == 40  # 20*2

    # Confirmar stock descontado
    book.refresh_from_db()
    assert book.copies_available == 3

    # Carrito debe estar vacío
    assert CartItem.objects.filter(user=user).count() == 0

    # Orden registrada
    assert Order.objects.filter(user=user).count() == 1
