import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from catalog.models import Book

User = get_user_model()

@pytest.mark.django_db
def test_favorite_crud():
    # Usuario y libro
    user = User.objects.create_user(username="u1", password="pass")
    book = Book.objects.create(title="X", author="A", genre="FIC", price=10)

    client = APIClient()
    # Sin auth debe 401
    resp = client.post("/api/favorites/", {"book": book.id})
    assert resp.status_code == 401

    # Autenticado
    client.force_authenticate(user)
    # Crear favorito
    resp = client.post("/api/favorites/", {"book": book.id})
    assert resp.status_code == 201
    fid = resp.json()["id"]

    # Listar favorito
    resp = client.get("/api/favorites/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Borrar favorito
    resp = client.delete(f"/api/favorites/{fid}/")
    assert resp.status_code == 204

    # Confirmar eliminado
    resp = client.get("/api/favorites/")
    assert resp.json() == []
