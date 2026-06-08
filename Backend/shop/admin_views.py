from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Sum

from .models import Category, Product, ProductVariant, Order
from .admin_serializers import (
    AdminCategorySerializer,
    AdminVariantSerializer,
    AdminProductListSerializer,
    AdminProductDetailSerializer,
    AdminOrderListSerializer,
    AdminOrderDetailSerializer,
    AdminOrderStatusSerializer,
    AdminLowStockSerializer,
)


# ── Dashboard ─────────────────────────────────────────────────────────────────

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        status_counts = {
            s: Order.objects.filter(status=s).count()
            for s in ["pending", "paid", "shipped", "delivered", "cancelled"]
        }
        recent_orders = (
            Order.objects.select_related("user")
            .prefetch_related("items")
            .order_by("-created_at")[:5]
        )
        low_stock = (
            ProductVariant.objects.select_related("product")
            .filter(stock__lte=5)
            .order_by("stock")[:10]
        )
        return Response({
            "total_products": Product.objects.count(),
            "available_products": Product.objects.filter(available=True).count(),
            "total_orders": Order.objects.count(),
            "orders_by_status": status_counts,
            "recent_orders": AdminOrderListSerializer(recent_orders, many=True).data,
            "low_stock_variants": AdminLowStockSerializer(low_stock, many=True).data,
        })


# ── Categories ────────────────────────────────────────────────────────────────

class AdminCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all().order_by("name")


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all()


# ── Products ──────────────────────────────────────────────────────────────────

class AdminProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        return AdminProductListSerializer if self.request.method == "GET" else AdminProductDetailSerializer

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related("category")
            .prefetch_related("variants")
            .order_by("-created_at")
        )
        if search := self.request.query_params.get("search"):
            qs = qs.filter(name__icontains=search)
        if category := self.request.query_params.get("category"):
            qs = qs.filter(category__id=category)
        available = self.request.query_params.get("available")
        if available is not None:
            qs = qs.filter(available=available.lower() == "true")
        return qs


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = AdminProductDetailSerializer
    queryset = Product.objects.select_related("category").prefetch_related("variants").all()


# ── Variants ──────────────────────────────────────────────────────────────────

class AdminVariantListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminVariantSerializer

    def get_queryset(self):
        return ProductVariant.objects.filter(product_id=self.kwargs["product_pk"])

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs["product_pk"])
        serializer.save(product=product)


class AdminVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminVariantSerializer
    queryset = ProductVariant.objects.all()


# ── Orders ────────────────────────────────────────────────────────────────────

class AdminOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminOrderListSerializer

    def get_queryset(self):
        qs = (
            Order.objects
            .select_related("user")
            .prefetch_related("items")
            .order_by("-created_at")
        )
        if status_filter := self.request.query_params.get("status"):
            qs = qs.filter(status=status_filter)
        return qs


class AdminOrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminOrderDetailSerializer
    queryset = Order.objects.select_related("user").prefetch_related(
        "items__variant__product"
    ).all()


class AdminOrderStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)
        serializer = AdminOrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AdminOrderDetailSerializer(order).data)
