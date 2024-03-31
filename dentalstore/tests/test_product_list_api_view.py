import os
from decimal import Decimal

# Это для запуска тестов по одному, из IDE:
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dentalstore.settings'
# import django
# django.setup()
# Остальные импорты
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from mixer.backend.django import mixer

from catalog.views import ProductListAPIView


class ProductListAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self._setup_view_and_uri()
        self.category = mixer.blend('catalog.ProductCategory', slug='category1')
        self.manufacturer = mixer.blend('catalog.Manufacturer', name='manufacturer1')
        self.tag = mixer.blend('catalog.TagProduct', slug='tag1')
        self.products = mixer.cycle(5).blend(
            'catalog.Product',
            category=self.category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        )

    def _setup_view_and_uri(self):
        self.view = ProductListAPIView.as_view()
        self.uri = '/products/paginations'

    def test_list(self):
        request = self.factory.get(self.uri)
        request.session = self.client.session
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            'Expected HTTP 200, received: {0} instead.'.format(response.status_code)
        )
        self.assertEqual(len(response.data['results']), 5, 'Expected 5 products.')

    def test_filter_by_min_price(self):
        min_price = min([product.price for product in self.products])
        request = self.factory.get(self.uri, {'min_price': min_price})
        request.session = self.client.session
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            'Expected HTTP 200, received: {0} instead.'.format(response.status_code),
        )
        for product in response.data['results']:
            self.assertGreaterEqual(float(product['price']), min_price, 'Product price is less than min_price')

    def test_filter_by_country(self):
        country = self.products[0].manufacturer_countries
        request = self.factory.get(self.uri, {'countries': country})
        request.session = self.client.session
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            'Expected HTTP 200, received: {0} instead.'.format(response.status_code),
        )
        for product in response.data['results']:
            self.assertIn(country, product['manufacturer_countries'], 'Country is incorrect')
