from django.db import models
from django.utils import timezone

class Book(models.Model):
    GENRE_CHOICES = [
        ("FIC", "Ficción"),
        ("NF",  "No Ficción"),
        ("SCI", "Ciencia"),
        ("TEC", "Tecnología"),
        ("BIO", "Biografía"),
        ("HIS", "Historia"),
        # Amplía según lo necesites
    ]

    title            = models.CharField("Título", max_length=255)
    subtitle         = models.CharField("Subtítulo", max_length=255, blank=True)
    author           = models.CharField("Autor", max_length=255)
    publisher        = models.CharField("Editorial", max_length=255, blank=True)
    publication_date = models.DateField("Fecha de publicación", blank=True, null=True)
    isbn_10          = models.CharField("ISBN‑10", max_length=10, unique=True, blank=True, null=True)
    isbn_13          = models.CharField("ISBN‑13", max_length=13, unique=True, blank=True, null=True)
    genre            = models.CharField("Género", max_length=3, choices=GENRE_CHOICES, default="FIC")
    language         = models.CharField("Idioma", max_length=30, default="Español")
    pages            = models.PositiveIntegerField("Páginas", blank=True, null=True)
    description      = models.TextField("Descripción", blank=True)
    cover            = models.ImageField("Portada", upload_to="covers/", blank=True)
    copies_total     = models.PositiveIntegerField("Ejemplares totales", default=1)
    copies_available = models.PositiveIntegerField("Ejemplares disponibles", default=1)
    price            = models.DecimalField("Precio (MXN)", max_digits=8, decimal_places=2, default=0)
    created_at       = models.DateTimeField("Creado", default=timezone.now)
    updated_at       = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return f"{self.title} – {self.author}"
