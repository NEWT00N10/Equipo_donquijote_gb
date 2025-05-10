from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from circulation.models import Loan, Reservation
from catalog.models import Book

class Command(BaseCommand):
    help = "Crea/actualiza grupos de roles y asigna permisos básicos."

    def handle(self, *args, **kwargs):
        # --- grupos ---
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        lib_group,   _ = Group.objects.get_or_create(name="Bibliotecario")
        cus_group,   _ = Group.objects.get_or_create(name="Cliente")

        # --- permisos específicos ---
        loan_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Loan)
        )
        resv_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Reservation)
        )
        book_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Book)
        )

        # --- asignaciones por grupo ---
        # Admin → todos
        admin_group.permissions.set(Permission.objects.all())

        # Bibliotecario → permisos de Libro, Loan y Reservation
        lib_group.permissions.set(book_perms | loan_perms | resv_perms)

        # Cliente → solo 'view_' de Book
        client_perms = book_perms.filter(codename__startswith="view_")
        cus_group.permissions.set(client_perms)

        self.stdout.write(self.style.SUCCESS("Grupos y permisos creados/actualizados"))
