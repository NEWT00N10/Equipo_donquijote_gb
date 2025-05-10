from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from orders.models import CartItem, Order, OrderItem
from orders.serializers import CartItemSerializer, OrderSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    """
    CRUD de items en carrito para el usuario autenticado.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.GenericViewSet):
    """
    Genera un pedido a partir del carrito actual y calcula total.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Obtener todos los items del carrito
        cart_items = CartItem.objects.filter(user=request.user).select_related("book")
        if not cart_items.exists():
            return Response({"detail": "Carrito vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular total sumando precio * cantidad
        total = sum(item.book.price * item.quantity for item in cart_items)

        # Crear Order
        order = Order.objects.create(user=request.user, total=total)

        # Crear OrderItems y vaciar carrito
        order_items = []
        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price_at_purchase=item.book.price
                )
            )
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
