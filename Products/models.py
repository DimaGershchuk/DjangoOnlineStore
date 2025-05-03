from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from Users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(350, 350)],
        format='JPEG',
        options={'quality': 95}
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField()
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 450)],
        format='JPEG',
        options={'quality': 95}
    )

    average_rating = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created'] #descending order
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['category']),
            models.Index(fields=['brand'])
        ]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product-detail', args=[self.slug])

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.product.name}: {self.rating}★"

