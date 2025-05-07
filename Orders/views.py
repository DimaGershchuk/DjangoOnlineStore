from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Cart.models import CartItem, Cart
from django.views.generic import ListView, DetailView
from .models import Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required
from .forms import ShippingForm


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'
    form_class = ShippingForm

    def get(self, request):
        # 1) Підтягуємо товари з кошика
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')

        # 2) Підтягуємо існуючу адресу (якщо була) або None
        order, _ = Order.objects.get_or_create(user=request.user)
        try:
            address = order.shipping_address
        except ShippingAddress.DoesNotExist:
            address = None

        form = self.form_class(instance=address)
        return render(request, self.template_name, {
            'cart_items': cart_items,
            'form': form,
            'order': order,
        })

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
        if not cart_items.exists():
            return redirect('cart-detail')

        # знову отримаємо або створимо Order
        order, _ = Order.objects.get_or_create(user=request.user)

        # обробляємо адресу
        try:
            address = order.shipping_address
        except ShippingAddress.DoesNotExist:
            address = None

        form = self.form_class(request.POST, instance=address)
        if not form.is_valid():
            # якщо форма невалідна, просто рендеримо обратно з помилками
            return render(request, self.template_name, {
                'cart_items': cart_items,
                'form': form,
                'order': order,
            })

        shipping = form.save(commit=False)
        shipping.order = order
        shipping.save()

        # створюємо OrderItem’и з поточними товарами
        total = 0
        # очищаємо попередні OrderItem-и, якщо треба:
        order.items.all().delete()
        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                price=ci.product.price,
                quantity=ci.quantity
            )
            total += ci.product.price * ci.quantity

        # зберігаємо загальну суму
        order.total_price = total
        order.save(update_fields=['total_price'])

        # тепер чистимо кошик
        cart_items.delete()

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


