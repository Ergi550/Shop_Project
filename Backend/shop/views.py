from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db import transaction
from .models import Category, Product, ProductVariant, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# --- Protected order endpoints ---

class MyOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the order, attaching the logged-in user
        order = serializer.save(user=request.user)

        # Build line items from the cart payload, snapshotting price
        items = request.data.get("items", [])
        if not items:
            order.delete()
            return Response({"detail": "No items provided."}, status=400)

        for item in items:
            variant = ProductVariant.objects.get(id=item["variant"])
            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=item["quantity"],
                price=variant.product.price,   # snapshot at purchase time
            )

        return Response(self.get_serializer(order).data, status=201)