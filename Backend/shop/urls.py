from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    MyOrderListView,
    OrderCreateView,
    RegisterView,
    VerifyEmailView,
    ResendVerificationCodeView,
    MeView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    path("categories/", CategoryListView.as_view(), name="category-list"),

    path("orders/", MyOrderListView.as_view(), name="my-orders"),
    path("orders/create/", OrderCreateView.as_view(), name="order-create"),

    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("auth/resend-code/", ResendVerificationCodeView.as_view(), name="resend-code"),
    path("auth/me/", MeView.as_view(), name="me"),
]
