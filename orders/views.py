from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token
from orders.models import CartItem
from orders.views_api import OrderViewSet

def cart_view(request):
    """
    Muestra los items del carrito y total provisional.
    """
    if not request.user.is_authenticated:
        return redirect("admin:login")

    # Obtener items y calcular línea y total
    items = CartItem.objects.filter(user=request.user).select_related("book")
    total = 0
    for item in items:
        item.line_total = item.book.price * item.quantity
        total += item.line_total

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total
    })

def checkout_view(request):
    """
    Ejecuta la creación de pedido vía API y muestra confirmación.
    """
    if not request.user.is_authenticated:
        return redirect("admin:login")
    # Llamar internamente al método create de OrderViewSet
    viewset = OrderViewSet.as_view({"post": "create"})
    response = viewset(request._request)  # WSGIRequest
    if response.status_code == 201:
        order = response.data
        return render(request, "cart/checkout.html", {"order": order})
    # En caso de error mostramos detalle
    return render(request, "cart/cart.html", {
        "items": CartItem.objects.filter(user=request.user).select_related("book"),
        "error": response.data.get("detail", "Error al procesar pedido.")
    })
