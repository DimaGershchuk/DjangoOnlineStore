from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import CartItem, WishList, Cart
from .serializers import CartItemSerializer, WishListItemSerializer
from Products.models import Product
from django.db.models import Prefetch


class CartDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product').all() # Витягую всі товари, які в корзині
        return render(request, 'cart/cart-detail.html', {'cart': cart, 'cart_items': cart_items})


class CartAddItemView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save(update_fields=['quantity'])
        return redirect('cart-detail')


class CartRemoveItemView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, item_id):
        cart = request.user.cart
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return redirect('cart-detail')


class WishListDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        wishlist, _ = WishList.objects.prefetch_related(Prefetch('products', queryset=Product.objects.select_related('category', 'brand'))).get_or_create(user=request.user) # Витягую всі товари для wishlist одни запитом через prefetch, тому що зв`язок M2M
        products = wishlist.products.all()
        return render(request, 'cart/wishlist-detail.html', {'wishlist': wishlist, 'products': products})


class WishListToggleView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return redirect('wishlist-detail')


class CartItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class CartItemDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)


class WishListRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = WishListItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        return self.request.user.wishlist


class WishListToggleAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, product_id):
        wishlist = request.user.wishlist
        product = generics.get_object_or_404(Product, pk=product_id)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            return Response({'status': 'removed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            wishlist.products.add(product)
            return Response({'status': 'added'}, status=status.HTTP_201_CREATED)