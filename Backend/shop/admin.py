from django.contrib import admin
from .models import Category,Product,ProductVariant,Order,OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug")
    prepopulated_fields = {"slug":("name",)}
class ProductVariantInline(admin.TabularInline):
    model=ProductVariant
    extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available", "created_at")
    list_filter = ("available", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline]

class OrderItemInline(admin.TabularInline):
    model =OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]