from rest_framework import serializers
from .models import Category, Product, ProductVariant, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


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


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

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
        