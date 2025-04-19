from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializers
from .filters import ProductFilter
from .pagination import ProductPageNumberPagination


class ProductListCreateAPIView(generics.ListAPIView):
    queryset = Product.object.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPageNumberPagination


class ProdutRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.object.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


