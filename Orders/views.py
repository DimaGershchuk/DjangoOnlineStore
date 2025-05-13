from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from Cart.models import CartItem, Cart
from django.views.generic import ListView, DetailView
from .models import Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required
from .forms import ShippingForm
from .serializers import OrderSerializer
from django.core.mail import EmailMessage
from .utils import generate_pdf_order


def send_order_confirmation(order):
    subject = f"You order #{order.pk} Confirmation"
    body = (
        f"Hi {order.user.username},\n\n"
        f"Thank you for your order #{order.pk}! "
        f"Please find attached your order confirmation.\n\n"
        "Best regards,\n"
        "Online Store Team"
    )
    pdf_data = generate_pdf_order(order)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=None,
        to=[order.user.email]
    )

    email.attach(f"order_{order.pk}.pdf", pdf_data)
    email.send(fail_silently=False)


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'
    form_class = ShippingForm

    def get(self, request):
        # 1) Підтягуємо товари з кошика
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')

        # 2) Підтягуємо існуючу адресу (якщо була) або None
        order, _ = Order.objects.get_or_create(user=request.user, status="PENDING")
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
        order, _ = Order.objects.get_or_create(user=request.user, status='PENDING')

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
        order.status = "PAID"
        order.save(update_fields=['total_price', 'status'])

        # тепер чистимо кошик
        cart_items.delete()

        send_order_confirmation(order)
        return redirect('order-success', pk=order.pk)


class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk, user=request.user)
        return render(request, 'orders/order_success.html', {'order': order})


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]



