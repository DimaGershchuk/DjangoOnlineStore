from django.db import models

from django.conf import settings
from Products.models import Product
User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Waiting for payment'),
        ('PAID', 'Paid successful'),
        ('SHIPPED', 'Delivered'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.pk} ({self.user})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} (Order # {self.order.pk})"


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    full_name = models.CharField(max_length=100)
    address_line1 = models.CharField("Address line 1", max_length=255)
    address_line2 = models.CharField("Address line 2", max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField("Postal / ZIP code", max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Shipping for Order #{self.order.pk}"




