from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Category, Product, ProductVariant, Order, OrderItem


# ── Categories ────────────────────────────────────────────────────────────────

class AdminCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "product_count"]

    def get_product_count(self, obj):
        return obj.products.count()


# ── Products ──────────────────────────────────────────────────────────────────

class AdminVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "size", "color", "stock"]


class AdminProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    variant_count = serializers.SerializerMethodField()
    total_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "price", "image", "available",
            "category", "category_name", "variant_count", "total_stock", "created_at",
        ]

    def get_variant_count(self, obj):
        return obj.variants.count()

    def get_total_stock(self, obj):
        from django.db.models import Sum
        result = obj.variants.aggregate(total=Sum("stock"))["total"]
        return result or 0


class AdminProductDetailSerializer(serializers.ModelSerializer):
    variants = AdminVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price", "image",
            "available", "category", "category_name", "variants",
            "created_at", "updated_At",
        ]
        extra_kwargs = {
            "slug": {"required": False},
            "image": {"required": False},
        }

    def validate(self, attrs):
        name = attrs.get("name") or (self.instance.name if self.instance else None)
        slug = attrs.get("slug")
        if not slug and name:
            base = slugify(name)
            candidate = base
            counter = 1
            exclude_pk = self.instance.pk if self.instance else None
            while Product.objects.filter(slug=candidate).exclude(pk=exclude_pk).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            attrs["slug"] = candidate
        return attrs


# ── Orders ────────────────────────────────────────────────────────────────────

class AdminOrderCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class AdminOrderItemVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "product_id", "product_name", "size", "color"]


class AdminOrderItemSerializer(serializers.ModelSerializer):
    variant = AdminOrderItemVariantSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ["id", "variant", "quantity", "price", "subtotal"]


class AdminOrderListSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(source="user.email", read_only=True)
    customer_name = serializers.SerializerMethodField()
    total = serializers.ReadOnlyField()
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "customer_email", "customer_name", "status",
            "total", "item_count", "created_at",
        ]

    def get_customer_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name or obj.user.username

    def get_item_count(self, obj):
        return obj.items.count()


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    customer = AdminOrderCustomerSerializer(source="user", read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id", "customer", "status", "total",
            "shipping_full_name", "shipping_address", "shipping_city",
            "shipping_postcode", "shipping_country", "shipping_phone",
            "items", "created_at", "updated_at",
        ]
        read_only_fields = [
            "customer", "total", "items", "created_at", "updated_at",
            "shipping_full_name", "shipping_address", "shipping_city",
            "shipping_postcode", "shipping_country", "shipping_phone",
        ]


class AdminOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]


# ── Dashboard ─────────────────────────────────────────────────────────────────

class AdminLowStockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "product_id", "product_name", "size", "color", "stock"]
