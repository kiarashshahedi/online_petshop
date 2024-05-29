from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from users_account.models import Customer
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"{self.user.username}'s Cart"

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=(('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')))
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class ShippingStatus(models.Model):
    status_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Shipping Status"
        verbose_name_plural = "Shipping Statuses"

    def __str__(self):
        return self.status_name

class Shipment(models.Model):
    order = models.OneToOneField(Order, related_name='shipment', on_delete=models.CASCADE)
    current_status = models.ForeignKey(ShippingStatus, related_name='shipments', on_delete=models.SET_NULL, null=True)
    tracking_number = models.CharField(max_length=100, unique=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

    def __str__(self):
        return f"Shipment for Order {self.order.id}"
