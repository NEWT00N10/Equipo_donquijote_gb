from django.db import models
from django.conf import settings
from catalog.models import Book

class Favorite(models.Model):
    """
    Relación de usuario ↔ libro marcado como favorito.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        related_name="favorites"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Libro favorito",
        related_name="favorited_by"
    )
    created_at = models.DateTimeField("Fecha de marcado", auto_now_add=True)

    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_book_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"
