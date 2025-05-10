from django.db import models
from django.conf import settings
from catalog.models import Book

class Review(models.Model):
    """
    Reseña de un libro: calificación (1-5) y comentario opcional.
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Libro reseñado"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Autor de la reseña"
    )
    rating = models.PositiveSmallIntegerField(
        "Calificación",
        choices=[(i, str(i)) for i in range(1, 6)],
    )
    comment = models.TextField("Comentario", blank=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "user"],
                name="unique_book_user_review"
            )
        ]

    def __str__(self):
        return f"{self.user.username} ({self.rating}/5) sobre '{self.book.title}'"
