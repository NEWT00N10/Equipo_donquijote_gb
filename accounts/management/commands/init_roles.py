from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Crea/actualiza los grupos de roles y asigna permisos básicos."

    def handle(self, *args, **kwargs):
        # --- crear grupos si no existen ---
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        lib_group,   _ = Group.objects.get_or_create(name="Bibliotecario")
        cus_group,   _ = Group.objects.get_or_create(name="Cliente")

        # --- obtener todos los permisos ---
        all_perms = Permission.objects.all()

        # Admin ⇒ todos los permisos
        admin_group.permissions.set(all_perms)

        # Bibliotecario ⇒ sólo permisos de apps 'catalog' (cuando exista) y 'accounts'
        catalog_accounts_perms = all_perms.filter(
            content_type__app_label__in=["catalog", "accounts"]
        )
        lib_group.permissions.set(catalog_accounts_perms)

        # Cliente ⇒ de momento ninguno (acceso controlado vía vistas)
        cus_group.permissions.clear()

        self.stdout.write(self.style.SUCCESS("Grupos y permisos creados/actualizados"))
