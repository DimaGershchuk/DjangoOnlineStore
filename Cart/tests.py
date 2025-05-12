from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Products.models import Category, Brand, ProductProxy
from Cart.models import Cart, CartItem, WishList

User = get_user_model()


class CartViewsTests(TestCase):
    def setUp(self):
        # 1) Створюємо тестового користувача і логінимо його
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='secret')
        self.client.login(username='alice', password='secret')

        # 2) Створюємо категорію/бренд/продукт
        self.cat = Category.objects.create(name='Sneakers', slug='sneakers', image='images/2.jpg')
        self.brand = Brand.objects.create(name='Adidas', slug='adidas')
        self.product = ProductProxy.objects.create(
            name='UltraBoost',
            slug='ultraboost',
            price=150,
            available=True,
            image='images/3.jpg',
            category=self.cat,
            brand=self.brand
        )

    def test_cart_detail_initially_empty(self):
        """GET /cart/ створює порожню корзину і рендерить шаблон із пустим списком."""
        resp = self.client.get(reverse('cart-detail'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart/cart-detail.html')
        # корзина створилась автоматично
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)
        # в контексті є пустий список cart_items
        self.assertIn('cart_items', resp.context)
        self.assertQuerySetEqual(resp.context['cart_items'], [])

    def test_cart_add_item(self):
        """POST /cart/add/<product_id>/ додає товар у кошик і редіректить."""
        url = reverse('cart-add', args=[self.product.id])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('cart-detail'))
        # у корзині з'явився один елемент із quantity=1
        cart = Cart.objects.get(user=self.user)
        items = cart.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product, self.product)
        self.assertEqual(items[0].quantity, 1)

        # двічі додати — лічильник збільшується
        self.client.post(url)
        items = cart.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].quantity, 2)

    def test_cart_remove_item(self):
        """POST /cart/remove/<item_id>/ видаляє CartItem."""
        # спочатку додаємо
        add_url = reverse('cart-add', args=[self.product.id])
        self.client.post(add_url)
        cart = Cart.objects.get(user=self.user)
        item = cart.items.first()

        remove_url = reverse('cart-remove', args=[item.id])
        resp = self.client.post(remove_url)
        self.assertRedirects(resp, reverse('cart-detail'))
        # елемент зник
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_wishlist_detail_initially_empty(self):
        """GET /cart/wishlist/ створює порожній WishList і рендерить його."""
        resp = self.client.get(reverse('wishlist-detail'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart/wishlist-detail.html')
        wl = WishList.objects.get(user=self.user)
        # products empty
        self.assertQuerySetEqual(wl.products.all(), [])

    def test_wishlist_toggle_add_and_remove(self):
        """POST /cart/wishlist/toggle/<product_id>/ додає і потім видаляє товар із списку улюблених."""
        toggle_url = reverse('wishlist-toggle', args=[self.product.id])

        # додати
        resp1 = self.client.post(toggle_url)
        self.assertRedirects(resp1, reverse('wishlist-detail'))
        wl = WishList.objects.get(user=self.user)
        self.assertIn(self.product, list(wl.products.all()))

        # видалити
        resp2 = self.client.post(toggle_url)
        self.assertRedirects(resp2, reverse('wishlist-detail'))
        wl.refresh_from_db()
        self.assertNotIn(self.product, list(wl.products.all()))

