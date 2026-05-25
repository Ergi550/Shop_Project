from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    MyOrderListView,
    OrderCreateView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("orders/", MyOrderListView.as_view(), name="my-orders"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),
]