from rest_framework import serializers
from django.conf import settings
from .models import Category, Product, ProductVariant, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "product_count", "preview_image"]

    def get_product_count(self, obj):
        return getattr(obj, 'product_count', 0)

    def get_preview_image(self, obj):
        image_path = getattr(obj, 'first_product_image', None)
        if not image_path:
            return None
        url = f'{settings.MEDIA_URL}{image_path}'
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "size", "color", "stock"]


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price",
            "image", "available", "category", "variants",
            "created_at",
        ]


class OrderItemVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "size", "color", "product_name", "product_slug", "product_image"]


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    variant = OrderItemVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "variant", "quantity", "price", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id", "user", "status", "total",
            "shipping_full_name", "shipping_address", "shipping_city",
            "shipping_postcode", "shipping_country", "shipping_phone",
            "items", "created_at",
        ]
        read_only_fields = ["user", "status"]
        