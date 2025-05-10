from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token
from orders.models import CartItem
from orders.views_api import OrderViewSet
from circulation.models import Loan

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
    - GET: redirige al carrito.
    - POST: crea el pedido y muestra confirmación.
    """
    if not request.user.is_authenticated:
        return redirect("admin:login")

    if request.method != "POST":
        # Si es GET u otro método, volvemos al carrito
        return redirect("cart-view")

    # POST: ejecutar la creación de pedido vía API
    viewset = OrderViewSet.as_view({"post": "create"})
    response = viewset(request)

    if response.status_code != 201:
        # Error → volver al carrito mostrando el mensaje
        items = CartItem.objects.filter(user=request.user).select_related("book")
        return render(request, "cart/cart.html", {
            "items": items,
            "error": response.data.get("detail", "Error al procesar pedido.")
        })

    # Pedido creado → mostrar resumen
    order = response.data
    return render(request, "cart/checkout.html", {
        "order": order
    })

def profile_view(request):
    """
    Muestra el dashboard de usuario con historial de pedidos y préstamos.
    """
    if not request.user.is_authenticated:
        return redirect("admin:login")

    # Pedidos del usuario
    orders = request.user.orders.all()

    # Préstamos activos y finalizados
    loans = Loan.objects.filter(borrower=request.user).order_by("-borrowed_at")

    return render(request, "profile.html", {
        "orders": orders,
        "loans": loans
    })
