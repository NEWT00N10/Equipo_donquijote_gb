from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from circulation.models import Reservation, Loan
from catalog.models import Book

@shared_task
def fulfill_oldest_reservation(book_id: int):
    """
    Convierte la reserva más antigua en préstamo si hay stock.
    Envía email al usuario beneficiado.
    """
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return "Libro no encontrado"

    # ¿Hay copias disponibles?
    if book.copies_available <= 0:
        return "Sin stock aún"

    # Reserva más antigua sin cumplir
    reservation = (
        Reservation.objects
        .filter(book=book, fulfilled=False)
        .order_by("created_at")
        .first()
    )
    if not reservation:
        return "No hay reservas"

    # Crear préstamo (Loan.save maneja stock)
    loan = Loan.objects.create(
        borrower=reservation.requester,
        book=book,
        due_date=timezone.now().date() + timezone.timedelta(days=7)
    )

    # Marcar reserva cumplida
    reservation.fulfilled = True
    reservation.save(update_fields=["fulfilled"])

    # Enviar email (consola en dev)
    subject = f"¡Tu reserva de '{book.title}' está lista!"
    msg = (
        f"Hola {loan.borrower.username},\n\n"
        f"Se ha creado un préstamo para tu reserva del libro '{book.title}'.\n"
        f"Fecha de devolución: {loan.due_date}.\n\n"
        "¡Disfrútalo!\nEquipo Don Quijote GB"
    )
    send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, [loan.borrower.email])

    return f"Reserva cumplida para {loan.borrower.username}"
