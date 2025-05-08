from django.urls import path
from .views import CheckoutView, OrderSuccessView, OrderListCreateView, OrderRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/<int:pk>/', OrderSuccessView.as_view(), name='order-success'),


    path('api/orders/', OrderListCreateView.as_view(), name='order-list'),
    path('api/order/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail')
]