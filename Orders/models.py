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

