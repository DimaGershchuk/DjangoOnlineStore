from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Cart.models import CartItem, Cart
from django.views.generic import ListView, DetailView
from .models import Order, OrderItem


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.user.cart
        items = cart.items.select_related('product').all()

        return render(request, 'orders/checkout.html', {'cart_items': items})

    def post(self, request):
        user = request.user
        cart = user.cart
        items = cart.items.select_related('product').all()

        if not items:
            return redirect('cart-detail')

        order = Order.objects.create(user=user)

        total = 0

        for ci in items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                price=ci.product.price,
                quantity=ci.quantity
            )
            total += ci.product.price * ci.quantity

        order.total_price = total
        order.save(update_fields=['total_price'])

        cart.items.all().delete()
        return redirect('order-success', pk=order.pk)


class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk, user=request.user)
        return render(request, 'orders/order_success.html', {'order': order})


#class OrderListView(LoginRequiredMixin, ListView):
    #model = Order
    #context_object_name = 'orders'
    #template_name = 'orders/order_list.html'

    #def get_queryset(self):
        #return Order.objects.filter(user = self.request.user).order_by('-create_at')


#class OrderDetailView(LoginRequiredMixin, DetailView):
    #model = Order
    #context_object_name = 'order'
    #template_name = 'orders/order_detail.html'


