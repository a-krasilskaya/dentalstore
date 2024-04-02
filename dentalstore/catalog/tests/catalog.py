import os
from abc import ABC
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from mixer.backend.django import mixer

from catalog.models import ProductCategory
from catalog.views import ProductListAPIView


class ProductListAPIViewTestBase(APITestCase, ABC):
    def setUp(self):
        self.factory = APIRequestFactory()
        self._setup_view_and_uri()
        self.category = mixer.blend('catalog.ProductCategory', slug='category1')
        self.manufacturer = mixer.blend('catalog.Manufacturer', name='manufacturer1')
        self.tag = mixer.blend('catalog.TagProduct', slug='tag1')
        self.products = []
        self.create_products(count=5)

    def _setup_view_and_uri(self):
        self.view = ProductListAPIView.as_view()
        self.uri = '/products/paginations'

    def create_products(self, count=1, category=None):
        if category is None:
            category = self.category
        self.products.append(mixer.cycle(count).blend(
            'catalog.Product',
            category=category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        ))

    def create_category(self, title: str | None = None, slug: str | None = None) -> ProductCategory:
        category = mixer.blend(
            'catalog.ProductCategory',
            title=title,
            slug=slug,
        )
        return category
