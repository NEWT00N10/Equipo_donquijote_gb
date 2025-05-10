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

@shared_task 
def remind_due_soon():
    """
    Envía un correo a los usuarios cuyos préstamos vencen
    dentro de 48 horas y aún no han sido devueltos.
    """
    from circulation.models import Loan  

    today = timezone.now().date()
    target_date = today + timezone.timedelta(days=2)

    loans = Loan.objects.filter(
        due_date=target_date,
        returned_at__isnull=True
    ).select_related("borrower", "book")

    count = 0
    for loan in loans:
        borrower = loan.borrower
        if not borrower.email:
            continue  # sin email no enviamos

        subject = f"Recordatorio: devuelve '{loan.book.title}' antes de {loan.due_date}"
        msg = (
            f"Hola {borrower.username},\n\n"
            f"Te recordamos que tu préstamo del libro '{loan.book.title}' "
            f"vence el {loan.due_date}. Por favor, devuélvelo a tiempo para evitar sanciones.\n\n"
            "¡Gracias!\nEquipo Don Quijote GB"
        )
        send_mail(subject, msg, "noreply@donquijotegb.local", [borrower.email])
        count += 1

    return f"{count} recordatorio(s) enviados"