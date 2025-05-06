from django.urls import path
from .views import CheckoutView, OrderSuccessView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/<int:pk>/', OrderSuccessView.as_view(), name='order-success'),

]