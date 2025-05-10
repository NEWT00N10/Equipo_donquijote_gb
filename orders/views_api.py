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
        # Paso 1: obtener los items del carrito del usuario
        cart_items = CartItem.objects.filter(user=request.user).select_related("book")
        if not cart_items.exists():
            return Response(
                {"detail": "Carrito vacío"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 2: validar stock para cada item
        insufficient = []
        for item in cart_items:
            if item.book.copies_available < item.quantity:
                insufficient.append({
                    "book_id": item.book.id,
                    "title": item.book.title,
                    "available": item.book.copies_available,
                    "requested": item.quantity
                })
        if insufficient:
            return Response(
                {
                    "detail": "Stock insuficiente para algunos libros",
                    "insufficient": insufficient
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 3: descontar stock
        total = 0
        for item in cart_items:
            book = item.book
            book.copies_available -= item.quantity
            book.save(update_fields=["copies_available"])
            total += book.price * item.quantity

        # Paso 4: crear Order y OrderItems
        order = Order.objects.create(user=request.user, total=total)
        order_items = [
            OrderItem(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price_at_purchase=item.book.price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Paso 5: vaciar carrito
        cart_items.delete()

        # Paso 6: serializar y devolver
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   