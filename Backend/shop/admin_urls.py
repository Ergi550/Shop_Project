from django.urls import path
from .admin_views import (
    AdminDashboardView,
    AdminCategoryListCreateView,
    AdminCategoryDetailView,
    AdminProductListCreateView,
    AdminProductDetailView,
    AdminVariantListCreateView,
    AdminVariantDetailView,
    AdminOrderListView,
    AdminOrderDetailView,
    AdminOrderStatusView,
)

urlpatterns = [
    path("dashboard/",                          AdminDashboardView.as_view(),           name="admin-dashboard"),

    path("categories/",                         AdminCategoryListCreateView.as_view(),  name="admin-category-list"),
    path("categories/<int:pk>/",                AdminCategoryDetailView.as_view(),      name="admin-category-detail"),

    path("products/",                           AdminProductListCreateView.as_view(),   name="admin-product-list"),
    path("products/<int:pk>/",                  AdminProductDetailView.as_view(),       name="admin-product-detail"),
    path("products/<int:product_pk>/variants/", AdminVariantListCreateView.as_view(),  name="admin-variant-list"),
    path("variants/<int:pk>/",                  AdminVariantDetailView.as_view(),       name="admin-variant-detail"),

    path("orders/",                             AdminOrderListView.as_view(),           name="admin-order-list"),
    path("orders/<int:pk>/",                    AdminOrderDetailView.as_view(),         name="admin-order-detail"),
    path("orders/<int:pk>/status/",             AdminOrderStatusView.as_view(),         name="admin-order-status"),
]
