from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ProductProxy


@receiver([post_save, post_delete], sender=ProductProxy)
def clear_product_list_cache(sender, **kwargs):
    cache.delete_pattern('*product-list*')
