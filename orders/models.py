from django.db import models
from django.conf import settings
from catalog.models import Book
from django.utils import timezone

class CartItem(models.Model):
    """
    Item suelto en el carrito de un usuario.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "book")
        verbose_name = "Elemento de carrito"
        verbose_name_plural = "Elementos de carrito"

    def __str__(self):
        return f"{self.quantity}× {self.book.title} para {self.user.username}"

class Order(models.Model):
    """
    Pedido que agrupa varios items de carrito.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.pk} de {self.user.username}"

class OrderItem(models.Model):
    """
    Relación de un pedido con cada libro y cantidad.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Elemento de pedido"
        verbose_name_plural = "Elementos de pedido"

    def __str__(self):
        return f"{self.quantity}× {self.book.title} en {self.order}"
