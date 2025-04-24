from django.urls import path

from .views import CartDetailView, CartAddItemView, WishListDetailView, WishListToggleView, CartRemoveItemView, CartItemDestroyAPIView, CartItemListCreateAPIView, WishListToggleAPIView, WishListRetrieveAPIView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/<int:product_id>/', CartAddItemView.as_view(), name='cart-add'),
    path('remove/<int:item_id>/', CartRemoveItemView.as_view(), name='cart-remove'),
    path('wishlist/', WishListDetailView.as_view(), name='wishlist-detail'),
    path('wishlist/toggle/<int:product_id>/', WishListToggleView.as_view(), name='wishlist-toggle'),

    # Api-endpoints

    path('api/cart/items/', CartItemListCreateAPIView.as_view(), name='api-cart-items'),
    path('api/cart/items/<int:item_id>', CartItemDestroyAPIView.as_view(), name='api-cart-item-delete'),
    path('api/wishlist/', WishListRetrieveAPIView.as_view(), name='api-wishlist'),
    path('api/wishlist/toggle/<int:product_id>/', WishListToggleAPIView.as_view(), name='api-wishlist-toggle'),
]
