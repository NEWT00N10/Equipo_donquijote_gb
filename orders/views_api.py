from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import CartItem, Order, OrderItem
from orders.serializers import CartItemSerializer, OrderSerializer
from .models import CartItem
from .serializers import CartItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    CRUD de items en el carrito para el usuario autenticado.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Solo los items del carrito del usuario actual
        return CartItem.objects.filter(user=self.request.user).select_related('book')

    def perform_create(self, serializer):
        # Al crear, asignar siempre el usuario actual
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.GenericViewSet):
    """
    Genera un pedido a partir del carrito actual y calcula el total.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def list(self, request):
        # Listar todos los pedidos del usuario
        orders = Order.objects.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        # 1) Obtener items del carrito
        cart_items = CartItem.objects.filter(user=request.user).select_related('book')
        if not cart_items.exists():
            return Response({'detail': 'Carrito vacío'}, status=status.HTTP_400_BAD_REQUEST)

        # 2) Validar stock
        insufficient = []
        for item in cart_items:
            if item.book.copies_available < item.quantity:
                insufficient.append({
                    'book_id': item.book.id,
                    'title': item.book.title,
                    'available': item.book.copies_available,
                    'requested': item.quantity,
                })
        if insufficient:
            return Response({
                    'detail': 'Stock insuficiente para algunos libros',
                    'insufficient': insufficient
                }, status=status.HTTP_400_BAD_REQUEST)

        # 3) Descontar stock y calcular total
        total = 0
        for item in cart_items:
            book = item.book
            book.copies_available -= item.quantity
            book.save(update_fields=['copies_available'])
            total += book.price * item.quantity

        # 4) Crear Order y sus OrderItems
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

        # 5) Vaciar carrito
        cart_items.delete()

        # 6) Devolver el pedido generado
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
