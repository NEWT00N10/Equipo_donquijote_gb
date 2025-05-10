from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.models import CartItem, Order, OrderItem
from circulation.models import Loan


@login_required
def cart_view(request):
    """
    Muestra los items del carrito y total provisional.
    """
    # Obtener items y calcular subtotal y total
    items = CartItem.objects.filter(user=request.user).select_related("book")
    total = sum(item.quantity * item.book.price for item in items)

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total
    })


@login_required
def checkout_view(request):
    """
    GET: muestra el resumen de checkout.
    POST: crea la orden, descuenta stock, vacía carrito y redirige a éxito.
    """
    items = CartItem.objects.filter(user=request.user).select_related("book")
    total = sum(item.quantity * item.book.price for item in items)

    if request.method == "POST":
        # 1) Crear la orden
        order = Order.objects.create(user=request.user, total=total)
        # 2) Crear cada OrderItem y descontar stock
        for item in items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            item.book.copies_available -= item.quantity
            item.book.save()
        # 3) Vaciar carrito
        items.delete()
        # 4) Redirigir a página de éxito
        return redirect("checkout-success", order.id)

    # GET
    return render(request, "cart/checkout.html", {
        "items": items,
        "total": total
    })


@login_required
def checkout_success_view(request, order_id):
    """
    Muestra la confirmación de pedido exitoso.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "cart/checkout_success.html", {
        "order": order
    })


@login_required
def profile_view(request):
    """
    Dashboard de usuario con historial de pedidos y préstamos.
    """
    orders = request.user.orders.all().order_by("-created_at")
    loans = Loan.objects.filter(borrower=request.user).order_by("-borrowed_at")
    return render(request, "profile.html", {
        "orders": orders,
        "loans": loans
    })


class OrderListView(LoginRequiredMixin, ListView):
    """
    Lista paginada de pedidos del usuario.
    """
    model = Order
    template_name = "orders/list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
