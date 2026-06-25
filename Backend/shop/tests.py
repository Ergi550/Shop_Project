from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Category, Order, OrderItem, Product, ProductVariant
from .admin_serializers import AdminProductDetailSerializer
from .serializers import CategorySerializer, ProductSerializer


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_category(name="Tops", slug="tops", description=""):
    return Category.objects.create(name=name, slug=slug, description=description)


def make_product(category, name="Test Shirt", slug="test-shirt", price="29.99", available=True):
    return Product.objects.create(
        category=category,
        name=name,
        slug=slug,
        price=Decimal(price),
        available=available,
    )


def make_variant(product, size="M", color="Blue", stock=10):
    return ProductVariant.objects.create(product=product, size=size, color=color, stock=stock)


def make_order(user, **kwargs):
    defaults = dict(
        shipping_full_name="John Doe",
        shipping_address="123 Main St",
        shipping_city="New York",
        shipping_postcode="10001",
        shipping_country="USA",
    )
    defaults.update(kwargs)
    return Order.objects.create(user=user, **defaults)


def make_order_item(order, variant, quantity=1, price=None):
    if price is None:
        price = variant.product.price
    return OrderItem.objects.create(order=order, variant=variant, quantity=quantity, price=price)


# ─────────────────────────────────────────────────────────────────────────────
# Model Unit Tests
# ─────────────────────────────────────────────────────────────────────────────

class CategoryModelTest(TestCase):
    def test_str(self):
        cat = make_category(name="Tops", slug="tops")
        self.assertEqual(str(cat), "Tops")

    def test_description_optional(self):
        cat = Category.objects.create(name="X", slug="x")
        self.assertEqual(cat.description, "")

    def test_unique_slug_enforced(self):
        make_category(name="Tops", slug="tops")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Tops Again", slug="tops")


class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = make_category()

    def test_str(self):
        p = make_product(self.cat, name="Test Shirt")
        self.assertEqual(str(p), "Test Shirt")

    def test_available_default_true(self):
        p = Product.objects.create(
            category=self.cat, name="Shirt", slug="shirt", price=Decimal("10.00")
        )
        self.assertTrue(p.available)

    def test_unique_slug_enforced(self):
        make_product(self.cat, name="A", slug="same-slug")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                category=self.cat, name="B", slug="same-slug", price=Decimal("5.00")
            )

    def test_category_protect_on_delete(self):
        make_product(self.cat)
        with self.assertRaises(ProtectedError):
            self.cat.delete()


class ProductVariantModelTest(TestCase):
    def setUp(self):
        self.cat = make_category()
        self.product = make_product(self.cat)

    def test_str_contains_size_and_color(self):
        v = make_variant(self.product, size="L", color="Red")
        self.assertIn("L", str(v))
        self.assertIn("Red", str(v))

    def test_unique_together_enforced(self):
        make_variant(self.product, size="M", color="Blue")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ProductVariant.objects.create(product=self.product, size="M", color="Blue", stock=5)

    def test_stock_default_zero(self):
        v = ProductVariant.objects.create(product=self.product, size="S", color="White")
        self.assertEqual(v.stock, 0)

    def test_different_color_same_size_allowed(self):
        make_variant(self.product, size="M", color="Blue")
        v2 = make_variant(self.product, size="M", color="Green")
        self.assertIsNotNone(v2.pk)

    def test_cascade_delete_with_product(self):
        v = make_variant(self.product)
        self.product.delete()
        self.assertFalse(ProductVariant.objects.filter(pk=v.pk).exists())


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.cat = make_category()
        self.product = make_product(self.cat, price="50.00")
        self.variant = make_variant(self.product)

    def test_str_contains_order_id(self):
        order = make_order(self.user)
        self.assertIn(str(order.id), str(order))

    def test_default_status_is_pending(self):
        order = make_order(self.user)
        self.assertEqual(order.status, "pending")

    def test_total_sums_item_subtotals(self):
        order = make_order(self.user)
        make_order_item(order, self.variant, quantity=2, price=Decimal("50.00"))
        self.assertEqual(order.total, Decimal("100.00"))

    def test_total_empty_order_is_zero(self):
        order = make_order(self.user)
        self.assertEqual(order.total, 0)

    def test_total_multiple_items(self):
        v2 = make_variant(self.product, size="L", color="Green", stock=5)
        order = make_order(self.user)
        make_order_item(order, self.variant, quantity=1, price=Decimal("50.00"))
        make_order_item(order, v2, quantity=3, price=Decimal("50.00"))
        self.assertEqual(order.total, Decimal("200.00"))


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass1234")
        self.cat = make_category()
        self.product = make_product(self.cat, price="25.00")
        self.variant = make_variant(self.product)
        self.order = make_order(self.user)

    def test_subtotal_is_price_times_quantity(self):
        item = make_order_item(self.order, self.variant, quantity=3, price=Decimal("25.00"))
        self.assertEqual(item.subtotal, Decimal("75.00"))

    def test_str_contains_quantity(self):
        item = make_order_item(self.order, self.variant, quantity=2)
        self.assertIn("2", str(item))


# ─────────────────────────────────────────────────────────────────────────────
# Serializer Unit Tests
# ─────────────────────────────────────────────────────────────────────────────

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.cat = make_category(name="Shoes", slug="shoes", description="All shoes")
        self.cat.product_count = 0
        self.cat.first_product_image = None

    def test_expected_fields_present(self):
        data = CategorySerializer(self.cat).data
        for field in ["id", "name", "slug", "description", "product_count", "preview_image"]:
            self.assertIn(field, data)

    def test_preview_image_is_none_without_image(self):
        data = CategorySerializer(self.cat).data
        self.assertIsNone(data["preview_image"])


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.cat = make_category()
        self.cat.product_count = 0
        self.cat.first_product_image = None
        self.product = make_product(self.cat)
        make_variant(self.product)

    def test_expected_fields_present(self):
        data = ProductSerializer(self.product).data
        for field in ["id", "name", "slug", "description", "price", "available", "category", "variants"]:
            self.assertIn(field, data)

    def test_variants_are_nested(self):
        data = ProductSerializer(self.product).data
        self.assertEqual(len(data["variants"]), 1)
        self.assertIn("size", data["variants"][0])
        self.assertIn("color", data["variants"][0])
        self.assertIn("stock", data["variants"][0])


class AdminProductDetailSerializerTest(TestCase):
    def setUp(self):
        self.cat = make_category()

    def test_slug_auto_generated_from_name(self):
        serializer = AdminProductDetailSerializer(data={
            "name": "Summer Dress", "price": "49.99",
            "category": self.cat.id, "available": True,
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.slug, "summer-dress")

    def test_slug_collision_increments_counter(self):
        Product.objects.create(
            category=self.cat, name="Summer Dress", slug="summer-dress", price=Decimal("49.99")
        )
        serializer = AdminProductDetailSerializer(data={
            "name": "Summer Dress", "price": "39.99",
            "category": self.cat.id, "available": True,
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.slug, "summer-dress-1")

    def test_explicit_slug_is_preserved(self):
        serializer = AdminProductDetailSerializer(data={
            "name": "My Product", "slug": "my-custom-slug",
            "price": "19.99", "category": self.cat.id, "available": True,
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.slug, "my-custom-slug")

    def test_partial_update_without_name_or_slug_regenerates_slug_from_existing_name(self):
        # Serializer always auto-generates slug from name when slug is absent,
        # even on partial update — so "old-slug" becomes slugify("Old Name") = "old-name".
        product = Product.objects.create(
            category=self.cat, name="Old Name", slug="old-slug", price=Decimal("10.00")
        )
        serializer = AdminProductDetailSerializer(
            instance=product, data={"price": "15.00"}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        product.refresh_from_db()
        self.assertEqual(product.slug, "old-name")


# ─────────────────────────────────────────────────────────────────────────────
# Public API: Products
# ─────────────────────────────────────────────────────────────────────────────

class ProductListViewTest(APITestCase):
    def setUp(self):
        self.cat1 = make_category(name="Tops", slug="tops")
        self.cat2 = make_category(name="Shoes", slug="shoes")
        make_product(self.cat1, name="Blue Tee", slug="blue-tee")
        make_product(self.cat1, name="Red Tee", slug="red-tee")
        make_product(self.cat2, name="Sneakers", slug="sneakers")
        make_product(self.cat1, name="Hidden", slug="hidden", available=False)

    def test_lists_available_products(self):
        res = self.client.get("/api/products/")
        self.assertEqual(res.status_code, 200)
        names = [p["name"] for p in res.data]
        self.assertIn("Blue Tee", names)
        self.assertIn("Sneakers", names)

    def test_excludes_unavailable_products(self):
        res = self.client.get("/api/products/")
        names = [p["name"] for p in res.data]
        self.assertNotIn("Hidden", names)

    def test_filter_by_category_slug(self):
        res = self.client.get("/api/products/?category=shoes")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Sneakers")

    def test_filter_returns_empty_for_unknown_category(self):
        res = self.client.get("/api/products/?category=nonexistent")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 0)

    def test_no_authentication_required(self):
        res = self.client.get("/api/products/")
        self.assertEqual(res.status_code, 200)


class ProductDetailViewTest(APITestCase):
    def setUp(self):
        self.cat = make_category()
        self.product = make_product(self.cat, name="Floral Dress", slug="floral-dress")

    def test_get_existing_product(self):
        res = self.client.get("/api/products/floral-dress/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "Floral Dress")

    def test_get_nonexistent_product_returns_404(self):
        res = self.client.get("/api/products/does-not-exist/")
        self.assertEqual(res.status_code, 404)

    def test_unavailable_product_returns_404(self):
        make_product(self.cat, name="Gone", slug="gone", available=False)
        res = self.client.get("/api/products/gone/")
        self.assertEqual(res.status_code, 404)

    def test_response_includes_variants(self):
        make_variant(self.product, size="S", color="Pink")
        res = self.client.get("/api/products/floral-dress/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("variants", res.data)
        self.assertEqual(len(res.data["variants"]), 1)


class CategoryListViewTest(APITestCase):
    def setUp(self):
        self.cat1 = make_category(name="Dresses", slug="dresses")
        self.cat2 = make_category(name="Bags", slug="bags")
        make_product(self.cat1, name="Blue Dress", slug="blue-dress")

    def test_lists_all_categories(self):
        res = self.client.get("/api/categories/")
        self.assertEqual(res.status_code, 200)
        names = [c["name"] for c in res.data]
        self.assertIn("Dresses", names)
        self.assertIn("Bags", names)

    def test_product_count_is_annotated(self):
        res = self.client.get("/api/categories/")
        dresses = next(c for c in res.data if c["slug"] == "dresses")
        self.assertEqual(dresses["product_count"], 1)

    def test_empty_category_has_zero_product_count(self):
        res = self.client.get("/api/categories/")
        bags = next(c for c in res.data if c["slug"] == "bags")
        self.assertEqual(bags["product_count"], 0)

    def test_no_authentication_required(self):
        res = self.client.get("/api/categories/")
        self.assertEqual(res.status_code, 200)


# ─────────────────────────────────────────────────────────────────────────────
# Auth: Register, JWT, Me
# ─────────────────────────────────────────────────────────────────────────────

class RegisterViewTest(APITestCase):
    def test_register_success(self):
        res = self.client.post("/api/auth/register/", {
            "username": "newuser", "email": "new@example.com", "password": "StrongPass123!"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["username"], "newuser")
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_stores_email(self):
        self.client.post("/api/auth/register/", {
            "username": "emailuser", "email": "test@shop.com", "password": "Pass1234!"
        }, format="json")
        user = User.objects.get(username="emailuser")
        self.assertEqual(user.email, "test@shop.com")

    def test_register_stores_first_and_last_name(self):
        self.client.post("/api/auth/register/", {
            "username": "fullname", "password": "Pass1234!",
            "first_name": "Jane", "last_name": "Doe",
        }, format="json")
        user = User.objects.get(username="fullname")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")

    def test_duplicate_username_returns_400(self):
        User.objects.create_user(username="taken", password="pass")
        res = self.client.post("/api/auth/register/", {
            "username": "taken", "password": "AnotherPass1!"
        }, format="json")
        self.assertEqual(res.status_code, 400)

    def test_missing_password_returns_400(self):
        res = self.client.post("/api/auth/register/", {"username": "nopass"}, format="json")
        self.assertEqual(res.status_code, 400)

    def test_missing_username_returns_400(self):
        res = self.client.post("/api/auth/register/", {"password": "SomePass123"}, format="json")
        self.assertEqual(res.status_code, 400)

    def test_email_used_as_username_when_no_username_given(self):
        res = self.client.post("/api/auth/register/", {
            "email": "only@email.com", "password": "Pass1234!"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(username="only@email.com").exists())


class JWTTokenTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username="jwtuser", password="TestPass123!")

    def test_obtain_token_success(self):
        res = self.client.post("/api/auth/token/", {
            "username": "jwtuser", "password": "TestPass123!"
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_obtain_token_wrong_password_returns_401(self):
        res = self.client.post("/api/auth/token/", {
            "username": "jwtuser", "password": "WrongPass"
        }, format="json")
        self.assertEqual(res.status_code, 401)

    def test_obtain_token_unknown_user_returns_401(self):
        res = self.client.post("/api/auth/token/", {
            "username": "nobody", "password": "Pass"
        }, format="json")
        self.assertEqual(res.status_code, 401)

    def test_refresh_token_returns_new_access_token(self):
        obtain = self.client.post("/api/auth/token/", {
            "username": "jwtuser", "password": "TestPass123!"
        }, format="json")
        res = self.client.post("/api/auth/token/refresh/", {
            "refresh": obtain.data["refresh"]
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)

    def test_invalid_refresh_token_returns_401(self):
        res = self.client.post("/api/auth/token/refresh/", {
            "refresh": "not-a-real-token"
        }, format="json")
        self.assertEqual(res.status_code, 401)


class MeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="meuser", password="pass1234",
            email="me@example.com", first_name="Alice", last_name="Smith",
        )
        self.client.force_authenticate(user=self.user)

    def test_returns_user_info(self):
        res = self.client.get("/api/auth/me/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["username"], "meuser")
        self.assertEqual(res.data["email"], "me@example.com")
        self.assertEqual(res.data["first_name"], "Alice")
        self.assertEqual(res.data["last_name"], "Smith")

    def test_includes_is_staff_field(self):
        res = self.client.get("/api/auth/me/")
        self.assertIn("is_staff", res.data)
        self.assertFalse(res.data["is_staff"])

    def test_admin_user_has_is_staff_true(self):
        admin = User.objects.create_superuser(username="boss", password="adminpass")
        self.client.force_authenticate(user=admin)
        res = self.client.get("/api/auth/me/")
        self.assertTrue(res.data["is_staff"])

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        res = self.client.get("/api/auth/me/")
        self.assertEqual(res.status_code, 401)


# ─────────────────────────────────────────────────────────────────────────────
# Orders: List & Create
# ─────────────────────────────────────────────────────────────────────────────

class MyOrderListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="pass1234")
        self.other = User.objects.create_user(username="otheruser", password="pass1234")
        self.order = make_order(self.user)
        self.other_order = make_order(self.other)

    def test_authenticated_user_sees_own_orders(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/orders/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], self.order.id)

    def test_unauthenticated_returns_401(self):
        res = self.client.get("/api/orders/")
        self.assertEqual(res.status_code, 401)

    def test_user_cannot_see_other_users_orders(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/orders/")
        ids = [o["id"] for o in res.data]
        self.assertNotIn(self.other_order.id, ids)


class OrderCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="pass1234")
        self.cat = make_category()
        self.product = make_product(self.cat, price="30.00")
        self.variant = make_variant(self.product, stock=5)
        self.client.force_authenticate(user=self.user)
        self.payload = {
            "shipping_full_name": "John Buyer",
            "shipping_address": "10 Shop St",
            "shipping_city": "London",
            "shipping_postcode": "E1 1AA",
            "shipping_country": "UK",
            "items": [{"variant": self.variant.id, "quantity": 2}],
        }

    def test_create_order_success(self):
        res = self.client.post("/api/orders/create/", self.payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_stock_is_deducted(self):
        self.client.post("/api/orders/create/", self.payload, format="json")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 3)

    def test_order_item_created_with_correct_quantity(self):
        res = self.client.post("/api/orders/create/", self.payload, format="json")
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)

    def test_price_is_snapshotted_from_product(self):
        res = self.client.post("/api/orders/create/", self.payload, format="json")
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.items.first().price, Decimal("30.00"))

    def test_order_status_defaults_to_pending(self):
        res = self.client.post("/api/orders/create/", self.payload, format="json")
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.status, "pending")

    def test_insufficient_stock_returns_400(self):
        payload = dict(self.payload, items=[{"variant": self.variant.id, "quantity": 99}])
        res = self.client.post("/api/orders/create/", payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_insufficient_stock_does_not_deduct_stock(self):
        payload = dict(self.payload, items=[{"variant": self.variant.id, "quantity": 99}])
        self.client.post("/api/orders/create/", payload, format="json")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 5)

    def test_nonexistent_variant_returns_400(self):
        payload = dict(self.payload, items=[{"variant": 99999, "quantity": 1}])
        res = self.client.post("/api/orders/create/", payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_empty_items_returns_400(self):
        payload = dict(self.payload, items=[])
        res = self.client.post("/api/orders/create/", payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        res = self.client.post("/api/orders/create/", self.payload, format="json")
        self.assertEqual(res.status_code, 401)

    def test_multiple_items_in_one_order(self):
        v2 = make_variant(self.product, size="L", color="Green", stock=3)
        payload = dict(self.payload, items=[
            {"variant": self.variant.id, "quantity": 1},
            {"variant": v2.id, "quantity": 2},
        ])
        res = self.client.post("/api/orders/create/", payload, format="json")
        self.assertEqual(res.status_code, 201)
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.items.count(), 2)

    def test_missing_shipping_fields_returns_400(self):
        res = self.client.post("/api/orders/create/", {
            "items": [{"variant": self.variant.id, "quantity": 1}]
        }, format="json")
        self.assertEqual(res.status_code, 400)


# ─────────────────────────────────────────────────────────────────────────────
# Admin: Dashboard
# ─────────────────────────────────────────────────────────────────────────────

class AdminDashboardViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.user = User.objects.create_user(username="regular", password="userpass")
        self.cat = make_category()

    def test_admin_can_access_dashboard(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/admin/dashboard/")
        self.assertEqual(res.status_code, 200)

    def test_dashboard_response_has_expected_keys(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/admin/dashboard/")
        for key in ["total_products", "available_products", "total_orders",
                    "orders_by_status", "recent_orders", "low_stock_variants"]:
            self.assertIn(key, res.data)

    def test_non_admin_returns_403(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get("/api/admin/dashboard/")
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_returns_401(self):
        res = self.client.get("/api/admin/dashboard/")
        self.assertEqual(res.status_code, 401)

    def test_product_counts_are_accurate(self):
        make_product(self.cat, name="P1", slug="p1")
        make_product(self.cat, name="P2", slug="p2", available=False)
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/admin/dashboard/")
        self.assertEqual(res.data["total_products"], 2)
        self.assertEqual(res.data["available_products"], 1)

    def test_orders_by_status_covers_all_statuses(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/admin/dashboard/")
        for s in ["pending", "paid", "shipped", "delivered", "cancelled"]:
            self.assertIn(s, res.data["orders_by_status"])

    def test_low_stock_variants_appear(self):
        product = make_product(self.cat, name="LowStock", slug="lowstock")
        make_variant(product, size="S", color="Red", stock=2)
        self.client.force_authenticate(user=self.admin)
        res = self.client.get("/api/admin/dashboard/")
        self.assertEqual(len(res.data["low_stock_variants"]), 1)


# ─────────────────────────────────────────────────────────────────────────────
# Admin: Categories
# ─────────────────────────────────────────────────────────────────────────────

class AdminCategoryViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=self.admin)
        self.cat = make_category(name="Accessories", slug="accessories")

    def test_list_categories(self):
        res = self.client.get("/api/admin/categories/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_create_category(self):
        res = self.client.post("/api/admin/categories/", {
            "name": "Bags", "slug": "bags", "description": "Hand bags"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Category.objects.filter(slug="bags").exists())

    def test_retrieve_category(self):
        res = self.client.get(f"/api/admin/categories/{self.cat.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "Accessories")

    def test_update_category(self):
        res = self.client.put(f"/api/admin/categories/{self.cat.id}/", {
            "name": "Updated Accessories", "slug": "accessories", "description": ""
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.name, "Updated Accessories")

    def test_partial_update_category(self):
        res = self.client.patch(f"/api/admin/categories/{self.cat.id}/", {
            "description": "New description"
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.description, "New description")

    def test_delete_category_without_products(self):
        cat2 = make_category(name="Hats", slug="hats")
        res = self.client.delete(f"/api/admin/categories/{cat2.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Category.objects.filter(slug="hats").exists())

    def test_nonexistent_category_returns_404(self):
        res = self.client.get("/api/admin/categories/99999/")
        self.assertEqual(res.status_code, 404)

    def test_non_admin_blocked(self):
        regular = User.objects.create_user(username="reg", password="pass")
        self.client.force_authenticate(user=regular)
        res = self.client.get("/api/admin/categories/")
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        res = self.client.get("/api/admin/categories/")
        self.assertEqual(res.status_code, 401)


# ─────────────────────────────────────────────────────────────────────────────
# Admin: Products
# ─────────────────────────────────────────────────────────────────────────────

class AdminProductViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=self.admin)
        self.cat = make_category()
        self.p1 = make_product(self.cat, name="Floral Dress", slug="floral-dress")
        self.p2 = make_product(self.cat, name="Striped Top", slug="striped-top")

    def test_list_products(self):
        res = self.client.get("/api/admin/products/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_search_filter(self):
        res = self.client.get("/api/admin/products/?search=Floral")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Floral Dress")

    def test_available_filter(self):
        make_product(self.cat, name="Hidden", slug="hidden-p", available=False)
        res = self.client.get("/api/admin/products/?available=true")
        names = [p["name"] for p in res.data]
        self.assertNotIn("Hidden", names)

    def test_category_filter(self):
        cat2 = make_category(name="Shoes", slug="shoes")
        make_product(cat2, name="Sneaker", slug="sneaker")
        res = self.client.get(f"/api/admin/products/?category={cat2.id}")
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Sneaker")

    def test_create_product_generates_auto_slug(self):
        res = self.client.post("/api/admin/products/", {
            "name": "New Blouse", "price": "45.00",
            "category": self.cat.id, "available": True,
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(slug="new-blouse").exists())

    def test_retrieve_product(self):
        res = self.client.get(f"/api/admin/products/{self.p1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], "Floral Dress")

    def test_partial_update_product(self):
        res = self.client.patch(f"/api/admin/products/{self.p1.id}/", {
            "available": False
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.p1.refresh_from_db()
        self.assertFalse(self.p1.available)

    def test_delete_product(self):
        res = self.client.delete(f"/api/admin/products/{self.p2.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.p2.id).exists())

    def test_nonexistent_product_returns_404(self):
        res = self.client.get("/api/admin/products/99999/")
        self.assertEqual(res.status_code, 404)

    def test_non_admin_blocked(self):
        regular = User.objects.create_user(username="reg2", password="pass")
        self.client.force_authenticate(user=regular)
        res = self.client.get("/api/admin/products/")
        self.assertEqual(res.status_code, 403)


# ─────────────────────────────────────────────────────────────────────────────
# Admin: Variants
# ─────────────────────────────────────────────────────────────────────────────

class AdminVariantViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=self.admin)
        self.cat = make_category()
        self.product = make_product(self.cat)
        self.variant = make_variant(self.product, size="S", color="White", stock=8)

    def test_list_variants_for_product(self):
        res = self.client.get(f"/api/admin/products/{self.product.id}/variants/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_create_variant(self):
        res = self.client.post(
            f"/api/admin/products/{self.product.id}/variants/",
            {"size": "XL", "color": "Black", "stock": 5}, format="json"
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue(
            ProductVariant.objects.filter(product=self.product, size="XL", color="Black").exists()
        )

    def test_retrieve_variant(self):
        res = self.client.get(f"/api/admin/variants/{self.variant.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["size"], "S")
        self.assertEqual(res.data["color"], "White")

    def test_update_variant_stock(self):
        res = self.client.patch(
            f"/api/admin/variants/{self.variant.id}/",
            {"stock": 20}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock, 20)

    def test_delete_variant(self):
        v2 = make_variant(self.product, size="L", color="Green", stock=2)
        res = self.client.delete(f"/api/admin/variants/{v2.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertFalse(ProductVariant.objects.filter(pk=v2.id).exists())

    def test_nonexistent_variant_returns_404(self):
        res = self.client.get("/api/admin/variants/99999/")
        self.assertEqual(res.status_code, 404)

    def test_list_only_returns_variants_for_that_product(self):
        other_product = make_product(self.cat, name="Other", slug="other-prod")
        make_variant(other_product, size="M", color="Red")
        res = self.client.get(f"/api/admin/products/{self.product.id}/variants/")
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["size"], "S")


# ─────────────────────────────────────────────────────────────────────────────
# Admin: Orders
# ─────────────────────────────────────────────────────────────────────────────

class AdminOrderViewTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.customer = User.objects.create_user(
            username="customer", password="pass", email="c@example.com"
        )
        self.client.force_authenticate(user=self.admin)
        self.cat = make_category()
        self.product = make_product(self.cat, price="20.00")
        self.variant = make_variant(self.product)
        self.order = make_order(self.customer)
        self.item = make_order_item(
            self.order, self.variant, quantity=2, price=Decimal("20.00")
        )

    def test_list_orders(self):
        res = self.client.get("/api/admin/orders/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_filter_orders_by_status(self):
        paid_order = make_order(self.customer)
        paid_order.status = "paid"
        paid_order.save()
        res = self.client.get("/api/admin/orders/?status=pending")
        statuses = [o["status"] for o in res.data]
        self.assertTrue(all(s == "pending" for s in statuses))
        self.assertEqual(len(res.data), 1)

    def test_retrieve_order_detail(self):
        res = self.client.get(f"/api/admin/orders/{self.order.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("items", res.data)
        self.assertIn("customer", res.data)

    def test_order_detail_includes_customer_info(self):
        res = self.client.get(f"/api/admin/orders/{self.order.id}/")
        self.assertEqual(res.data["customer"]["username"], "customer")
        self.assertEqual(res.data["customer"]["email"], "c@example.com")

    def test_order_list_shows_correct_total(self):
        res = self.client.get("/api/admin/orders/")
        self.assertEqual(Decimal(str(res.data[0]["total"])), Decimal("40.00"))

    def test_update_order_status_to_shipped(self):
        res = self.client.patch(
            f"/api/admin/orders/{self.order.id}/status/",
            {"status": "shipped"}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "shipped")

    def test_update_order_status_to_cancelled(self):
        res = self.client.patch(
            f"/api/admin/orders/{self.order.id}/status/",
            {"status": "cancelled"}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "cancelled")

    def test_invalid_status_returns_400(self):
        res = self.client.patch(
            f"/api/admin/orders/{self.order.id}/status/",
            {"status": "not-a-status"}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    def test_nonexistent_order_status_update_returns_404(self):
        res = self.client.patch(
            "/api/admin/orders/99999/status/",
            {"status": "shipped"}, format="json"
        )
        self.assertEqual(res.status_code, 404)

    def test_non_admin_blocked(self):
        regular = User.objects.create_user(username="reg3", password="pass")
        self.client.force_authenticate(user=regular)
        res = self.client.get("/api/admin/orders/")
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        res = self.client.get("/api/admin/orders/")
        self.assertEqual(res.status_code, 401)
