from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import ProductProxy, Category, Brand, Review
from .forms import ReviewForm

User = get_user_model()


class ProductViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.brand = Brand.objects.create(name="Nike", slug="nike")
        cls.cat1 = Category.objects.create(name="Sneakers", slug="sneakers", image="images/2.jpg")
        # create 12 products to test pagination (paginate_by=10)
        for i in range(12):
            ProductProxy.objects.create(
                name=f"Prod{i}",
                slug=f"prod-{i}",
                price=10 + i,
                available=True,
                image="images/2.jpg",
                category=cls.cat1,
                brand=cls.brand
            )

    def test_product_list_view_status_and_context(self):
        resp = self.client.get(reverse('product-list'))
        self.assertEqual(resp.status_code, 200)
        # paginate_by =10 so page1 has 10
        self.assertEqual(len(resp.context['products']), 10)
        self.assertIn('categories', resp.context)
        self.assertIn('q', resp.context)

    def test_product_list_view_second_page(self):
        resp = self.client.get(reverse('product-list'), {'page': 2})
        self.assertEqual(resp.status_code, 200)
        # remaining 2 on page2
        self.assertEqual(len(resp.context['products']), 2)

    def test_product_list_filter_by_category(self):
        # create a second category+product
        other = Category.objects.create(name="Boots", slug="boots", image="images/2.jpg")
        ProductProxy.objects.create(
            name="BootProd", slug="bootprod", price=50, available=True,
            image="images/2.jpg", category=other, brand=self.brand
        )
        resp = self.client.get(reverse('product-list'), {'category': 'boots'})
        self.assertEqual(resp.status_code, 200)
        prods = resp.context['products']
        self.assertEqual(len(prods), 1)
        self.assertEqual(prods[0].category.slug, 'boots')

    def test_product_detail_and_review_post(self):
        user = User.objects.create_user(username='rvw', password='pw')
        self.client.login(username='rvw', password='pw')
        prod = ProductProxy.objects.first()
        url = reverse('product-detail', kwargs={'slug': prod.slug})
        # GET detail
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('reviews', resp.context)
        self.assertQuerySetEqual(resp.context['reviews'], [])

        # POST a review
        data = {'rating': 4, 'comment': 'Great!'}
        resp2 = self.client.post(url, data)
        # should redirect back
        self.assertEqual(resp2.status_code, 302)
        # now GET should show it
        resp3 = self.client.get(url)
        reviews = resp3.context['reviews']
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].comment, 'Great!')
        self.assertEqual(reviews[0].user.username, 'rvw')


class ProductApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='api', password='pw')
        self.client.force_authenticate(self.user)
        self.brand = Brand.objects.create(name="Adidas", slug="adidas")
        self.cat = Category.objects.create(name="Tees", slug="tees", image="images/2.jpg")
        self.prod1 = ProductProxy.objects.create(
            name="Tee1", slug="tee1", price=20, available=True,
            image="images/2.jpg", category=self.cat, brand=self.brand
        )
        self.prod2 = ProductProxy.objects.create(
            name="Tee2", slug="tee2", price=30, available=True,
            image="images/3.jpg", category=self.cat, brand=self.brand
        )

    def test_api_list_products(self):
        url = reverse('api-product-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # paginated
        self.assertIn('results', data)
        names = {item['name'] for item in data['results']}
        self.assertIn('Tee1', names)
        self.assertIn('Tee2', names)

    def test_api_filter_q_and_category(self):
        # filter by q
        resp = self.client.get(reverse('api-product-list'), {'q': 'tee1'})
        data = resp.json()
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['slug'], 'tee1')

    def test_api_retrieve_update_destroy(self):
        url = reverse('api-product-detail', args=[self.prod1.pk])
        # retrieve
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['name'], 'Tee1')
        # update
        resp2 = self.client.patch(url, {'price': 25}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.prod1.refresh_from_db()
        self.assertEqual(str(self.prod1.price), '25.00')
        # destroy
        resp3 = self.client.delete(url)
        self.assertEqual(resp3.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProductProxy.objects.filter(pk=self.prod1.pk).exists())


class ReviewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='rev', password='pw')
        self.client.force_authenticate(self.user)
        self.brand = Brand.objects.create(name="Puma", slug="puma")
        self.cat = Category.objects.create(name="Caps", slug="caps", image="c.jpg")
        self.prod = ProductProxy.objects.create(
            name="Cap", slug="cap", price=15, available=True,
            image="cap.jpg", category=self.cat, brand=self.brand
        )

    def test_review_list_and_create(self):
        url = reverse('product-reviews', kwargs={'product_pk': self.prod.pk})
        # initially empty but paginated
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['results'], [])

        # create
        resp2 = self.client.post(url, {'rating': 5, 'comment': 'Nice cap!', 'product': self.prod.pk})
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        # list now has one
        resp3 = self.client.get(url)
        self.assertEqual(resp3.json()['count'], 1)
        item = resp3.json()['results'][0]
        self.assertEqual(item['rating'], 5)
        self.assertEqual(item['comment'], 'Nice cap!')
        self.assertEqual(item['user'], self.user.username)
