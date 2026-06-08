from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, OuterRef, Q, Subquery
from .models import Category, Product, ProductVariant, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)



class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(available=True).select_related('category').prefetch_related('variants')
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(available=True).select_related('category').prefetch_related('variants')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        first_image = Product.objects.filter(
            category=OuterRef('pk'),
            available=True,
        ).exclude(image='').values('image')[:1]
        return Category.objects.annotate(
            product_count=Count('products', filter=Q(products__available=True)),
            first_product_image=Subquery(first_image),
        )


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
            try:
                variant = ProductVariant.objects.select_related('product').get(id=item["variant"])
            except ProductVariant.DoesNotExist:
                order.delete()
                return Response({"detail": f"Variant {item['variant']} not found."}, status=400)

            quantity = item["quantity"]
            if variant.stock < quantity:
                order.delete()
                return Response(
                    {"detail": f"'{variant.product.name}' only has {variant.stock} item(s) in stock."},
                    status=400,
                )

            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=quantity,
                price=variant.product.price,
            )
            variant.stock -= quantity
            variant.save(update_fields=["stock"])

        return Response(self.get_serializer(order).data, status=201)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username') or request.data.get('email')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not username or not password:
            return Response({'detail': 'Username and password required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already taken.'}, status=400)

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
        )
        return Response({'id': user.id, 'username': user.username, 'email': user.email}, status=201)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            'id': u.id, 'username': u.username, 'email': u.email,
            'first_name': u.first_name, 'last_name': u.last_name,
            'is_staff': u.is_staff,
        })