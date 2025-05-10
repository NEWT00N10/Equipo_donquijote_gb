from django.db import models
from django.conf import settings
from django.utils import timezone
from catalog.models import Book

User = settings.AUTH_USER_MODEL  # referencia al modelo CustomUser

class Loan(models.Model):
    """
    Un préstamo activo en el sistema.
    Regla clave: copies_available del libro se reduce al crear
    y se incrementa al marcar como devuelto.
    """
    borrower        = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    book            = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Libro")
    borrowed_at     = models.DateTimeField("Fecha de préstamo", default=timezone.now)
    due_date        = models.DateField("Fecha límite", help_text="YYYY‑MM‑DD")
    returned_at     = models.DateTimeField("Devuelto", blank=True, null=True)

    class Meta:
        ordering = ["-borrowed_at"]
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        constraints = [
            models.UniqueConstraint(
                fields=["borrower", "book", "returned_at"],
                name="unique_active_loan",
                condition=models.Q(returned_at__isnull=True),
            )
        ]

    def __str__(self):
        return f"{self.book.title} → {self.borrower} ({self.borrowed_at:%d‑%m})"

    # --- lógica de stock ---
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        # Cargar libro desde BD para leer copies_available actualizado
        book_obj = Book.objects.select_for_update().get(pk=self.book.pk)

        if is_new:
            if book_obj.copies_available <= 0:
                raise ValueError("No hay ejemplares disponibles de este libro.")
            book_obj.copies_available -= 1
            book_obj.save()
        else:
            # Si se marca como devuelto por primera vez
            if self.returned_at and not Loan.objects.get(pk=self.pk).returned_at:
                book_obj.copies_available += 1
                book_obj.save()
        super().save(*args, **kwargs)


class Reservation(models.Model):
    """
    Una reserva de un libro cuando no hay copias disponibles.
    Cuando se devuelve un ejemplar, la reserva más antigua se convierte en Loan.
    """
    requester       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    book            = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Libro")
    created_at      = models.DateTimeField("Fecha de reserva", default=timezone.now)
    fulfilled       = models.BooleanField("Atendida", default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "book", "fulfilled"],
                name="unique_active_reservation",
                condition=models.Q(fulfilled=False),
            )
        ]

    def __str__(self):
        return f"Reserva {self.book.title} – {self.requester}"
