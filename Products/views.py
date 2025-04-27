from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView

from .models import Product, Category
from .serializers import ProductSerializers
from .filters import ProductFilter
from .pagination import ProductPageNumberPagination


def home_view(request):
    categories = Category.objects.all()
    return render(request, 'home-page.html', {'categories': categories})


class ProductListCreateAPIView(generics.ListAPIView):
    queryset = Product.objects.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPageNumberPagination


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListView(ListView):
    model = Product
    template_name = 'products/product-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return (
            Product.objects.filter(available=True).select_related('category', 'brand')
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    slug_field = 'slug' # slug_url_kwarg — «де взяти» значення вхідного параметра з адреси (ключ у kwargs), slug_field — «по якому» полю моделі це значення шукати.
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_queryset(self):
        return (
            Product.objects.select_related('category', 'brand')
        )
