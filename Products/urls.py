from django.urls import path

from .views import ProductListView, ProductDetailView, ProductListAPIView, ProductRetrieveUpdateDestroyAPIView, home_view, ReviewListCreateApiView

urlpatterns = [
    path('', home_view, name='home-page'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    #  Api-endpoints
    path('api/products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='api-product-detail'),
    path('api/products/<int:product_pk>/reviews/', ReviewListCreateApiView.as_view(), name='product-reviews')
]