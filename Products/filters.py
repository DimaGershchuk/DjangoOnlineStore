from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='exact'
    )

    brand = filters.CharFilter(
        field_name='brand__slug', lookup_expr='exact'
    )
    price_min = filters.NumberFilter(
        field_name='price', lookup_expr='gte', label='Min price'
    )
    price_max = filters.NumberFilter(
        field_name='price', lookup_expr='lte', label='Max price'
    )
    available = filters.BooleanFilter(
        field_name='available'
    )

    class Meta:
        model = Product
        fields = ['category', 'brand', 'price_min', 'price_max', 'available']
