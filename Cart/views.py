from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Products.models import Product
from .models import CartItem, WishList


class CartDetailView(LoginRequiredMixin, View):

    def get(self, request):
        cart = request.user.cart
        return render(request, 'cart/cart-detail.html', {'cart': cart})


class CartAddItemView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = request.user.cart
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save(update_fields=['quantity'])
        return redirect('cart-detail')


class CartRemoveItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = request.user.cart
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return redirect('cart-detail')


class WishListDetailView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist = request.user.wishlist
        return render(request, 'cart/wishlist-detail.html', {'wishlist': wishlist})


class WishListToggleView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        wishlist = request.user.wishlist
        product = get_object_or_404(Product, id=product_id)

        if product in wishlist.objects.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return redirect('wishlist-detail')


