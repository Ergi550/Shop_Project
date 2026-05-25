from django.db   import models


class Category(models.Model):
  name=models.CharField(max_length=100)
  slug=models.SlugField(max_length=120,unique=True)
  description=models.TextField(blank=True)

  class Meta:
    verbose_name_plural="Categories"

  def __str__(self):
    return self.name
class Product(models.Model):
  
  category = models.ForeignKey(Category,related_name='products', on_delete=models.PROTECT)
  name = models.CharField(max_length=200)
  slug = models.CharField(max_length=220,unique=True,blank=True)
  description= models.CharField(blank=True)
  price=models.DecimalField(max_digits=10,decimal_places=2)
  image=models.ImageField(upload_to="products/",blank=True,null=True)
  available=models.BooleanField(default=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_At=models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


  
class ProductVariant(models.Model):
  product = models.ForeignKey(Product,related_name="variants",on_delete=models.CASCADE)
  size = models.CharField(max_length=20,blank=True)
  color = models.CharField(max_length=50,blank=True)
  stock=models.PositiveIntegerField(default=0)

  class Meta:
    unique_together=("product","size","color")
  def _str__(self):
   return  f"{self.product.name} — {self.size}/{self.color}"
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.PROTECT
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    shipping_full_name=models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} — {self.user}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        ProductVariant, related_name="order_items", on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} × {self.variant}"

    @property
    def subtotal(self):
        return self.price * self.quantity