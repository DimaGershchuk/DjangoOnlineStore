from django.urls import path

from .views import ProductListView, ProductDetailView, ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    #  Api-endpoints
    path('api/products/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail')
]