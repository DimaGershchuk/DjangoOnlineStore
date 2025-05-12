import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from Cart.models import Cart, CartItem
from Products.models import ProductProxy, Category, Brand
from Orders.models import Order, OrderItem, ShippingAddress
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from Orders.serializers import OrderSerializer


User = get_user_model()


class OrdersViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user
        cls.user = User.objects.create_user(username='testuser', password='pass123')
        # create category and brand and a product
        cls.brand = Brand.objects.create(name='TestBrand', slug='testbrand')
        cls.category = Category.objects.create(name='TestCat', slug='testcat', image='images/2.jpg')
        cls.product = ProductProxy.objects.create(
            name='TestProduct', slug='testproduct', price=50.00, available=True,
            image='images/3.jpg', category=cls.category, brand=cls.brand
        )

    def setUp(self):
        # login and ensure empty cart
        self.client = Client()
        self.client.login(username='testuser', password='pass123')
        # get or create cart
        self.cart, _ = Cart.objects.get_or_create(user=self.user)

    def test_checkout_get_renders_form_and_empty_items(self):
        url = reverse('checkout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # context has cart_items empty and form
        self.assertIn('cart_items', resp.context)
        self.assertQuerySetEqual(resp.context['cart_items'], [])
        self.assertIn('form', resp.context)
        self.assertIn('order', resp.context)
        # no Order created yet
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_checkout_post_creates_order_and_shipping_address_and_items_and_clears_cart(self):
        # add an item to cart
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        url = reverse('checkout')
        data = {
            'full_name': 'John Doe',
            'address_line1': '123 Main St',
            'address_line2': '',
            'city': 'CityX',
            'postal_code': '12345',
            'country': 'CountryY',
            'phone_number': '555-1234',
        }
        resp = self.client.post(url, data)
        # should redirect to order-success
        self.assertEqual(resp.status_code, 302)
        order = Order.objects.get(user=self.user, status='PENDING')
        # ShippingAddress created correctly
        self.assertEqual(order.shipping_address.full_name, 'John Doe')
        # OrderItem created and total_price set
        items = OrderItem.objects.filter(order=order)
        self.assertEqual(items.count(), 1)
        item = items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(order.total_price, 100.00)
        # Cart cleared
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

    def test_order_success_view_shows_order(self):
        # manually create an order
        order = Order.objects.create(user=self.user, total_price=75.00, status='PENDING')
        url = reverse('order-success', kwargs={'pk': order.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f"Order №{order.pk}")
        self.assertContains(resp, "$75.00")


# API tests for Orders
class OrdersApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pw123')
        self.client.force_authenticate(user=self.user)
        # setup product for items
        self.brand = Brand.objects.create(name='BrandX', slug='brandx')
        self.cat = Category.objects.create(name='CatX', slug='catx', image='images/2.jpg')
        self.product = ProductProxy.objects.create(
            name='ProdX', slug='prodx', price=30.0, available=True,
            image='images/3.jpg', category=self.cat, brand=self.brand
        )
        # create an order with an item
        self.order = Order.objects.create(user=self.user, total_price=30.0, status='PENDING')
        OrderItem.objects.create(order=self.order, product=self.product, price=30.0, quantity=1)

    def test_api_list_orders(self):
        url = reverse('order-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # assuming pagination
        if 'results' in data:
            results = data['results']
        else:
            results = data
        self.assertTrue(any(o['id'] == self.order.id for o in results))

    def test_api_retrieve_update_destroy_order(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        # retrieve
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['id'], self.order.id)
        # update status
        resp2 = self.client.patch(url, {'status': 'PAID'}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'PENDING')
        # delete
        resp3 = self.client.delete(url)
        self.assertEqual(resp3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())



