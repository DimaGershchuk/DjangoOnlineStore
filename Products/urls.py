from django.urls import path

from .views import ProductListView, ProductDetailView, ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, home_view

urlpatterns = [
    path('', home_view, name='home-page'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    #  Api-endpoints
    path('api/products/', ProductListCreateAPIView.as_view(), name='api-product-list'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='api-product-detail')
]