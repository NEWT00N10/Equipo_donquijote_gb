from orders.views_api import CartViewSet
router.register(r'cart', CartViewSet, basename='cart')