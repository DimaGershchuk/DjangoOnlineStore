from django.urls import path

from .views import CartDetailView, CartAddItemView, WishListDetailView, WishListToggleView, CartRemoveItemView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/<int:product_id>/', CartAddItemView.as_view(), name='cart-add'),
    path('remove/<int:item_id>/', CartRemoveItemView.as_view(), name='cart-remove'),
    path('wishlist/', WishListDetailView.as_view(), name='wishlist-detail'),
    path('wishlist/toggle/<int:product_id>/', WishListToggleView.as_view(), name='wishlist-toggle'),
]
