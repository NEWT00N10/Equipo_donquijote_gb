from django.db.models.signals import post_save
from django.dispatch import receiver
from circulation.models import Loan
from circulation.tasks import fulfill_oldest_reservation

@receiver(post_save, sender=Loan)
def loan_post_save(sender, instance: Loan, created: bool, **kwargs):
    """
    Si un Loan existente cambia su returned_at de None a valor => devuelve libro.
    Entonces lanzamos la task para cumplir la reserva.
    """
    if not created:
        # Valor previo de returned_at
        old = Loan.objects.get(pk=instance.pk)
        if old.returned_at is None and instance.returned_at is not None:
            fulfill_oldest_reservation.delay(instance.book_id)
