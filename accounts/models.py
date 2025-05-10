from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extiende el usuario básico de Django con un campo 'role'.
    Admin = control total, Bibliotecario = gestiona inventario / préstamos,
    Cliente = usuario final que pide libros.
    """
    class Roles(models.TextChoices):
        ADMIN        = "ADMIN",  "Administrador global"
        LIBRARIAN    = "LIB",    "Bibliotecario"
        CUSTOMER     = "CUS",    "Cliente"

    role = models.CharField(
        max_length=5,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
        help_text="Rol que determina permisos por defecto",
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
