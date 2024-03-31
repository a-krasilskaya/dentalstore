import os
from decimal import Decimal
from random import randint

# Это для запуска тестов по одному, из IDE:
# os.environ['DJANGO_SETTINGS_MODULE'] = 'dentalstore.settings'
# import django
# django.setup()
# Остальные импорты
from catalog.views import ProductSearchAPIView
from dentalstore.settings import MIN_SEARCH_STRING_LENGTH
from tests.test_product_list_api_view import ProductListAPIViewTest
from mixer.backend.django import mixer
from catalog.utils import transliterate


class ProductSearchAPIViewTest(ProductListAPIViewTest):
    def setUp(self):
        super().setUp()

    def _setup_view_and_uri(self):
        self.view = ProductSearchAPIView.as_view()
        self.uri = '/products/search/'

    def test_search_title_and_description(self):
        self.products.append(mixer.blend(
            'catalog.Product',
            title='тест_987',
            description='Тестирование описания продукта',
            category=self.category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        ))

        search_strings = [
            self._generate_search_data(self.products, 'title'),
            'test_987',
            'тест_987',
            'produkta',
            'описания продукта'
        ]
        for search_string in search_strings:
            uri = f'{self.uri}?q={search_string}'
            request = self.factory.get(uri)
            request.session = self.client.session
            response = self.view(request)
            self.assertEqual(
                response.status_code,
                200,
                'Expected HTTP 200, received: {0} instead.'.format(response.status_code)
            )
            response_data = response.data['results']
            if len(response_data) == 0:
                pass
            self.assertGreaterEqual(len(response_data), 0, 'Not found record in response')
            for product in response_data:
                result_found_in_string = f'{product["title"]} {product["description"]}'
                result_found_in_string = ''.join(transliterate(result_found_in_string))
                self.assertIn(
                    search_string,
                    result_found_in_string,
                    f'String {search_string} not found in product.title'
                )

    def test_search_category(self):
        category = mixer.blend(
            'catalog.ProductCategory',
            title='Герметики',
            slug='category_test_search',
        )
        self.products.append(mixer.blend(
            'catalog.Product',
            title='тест_987',
            description='Тестирование описания продукта',
            category=category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        ))

        search_strings = [
            'герметики',
            'germetiki',
        ]
        for search_string in search_strings:
            uri = f'{self.uri}?q={search_string}'
            request = self.factory.get(uri)
            request.session = self.client.session
            response = self.view(request)
            self.assertEqual(
                response.status_code,
                200,
                'Expected HTTP 200, received: {0} instead.'.format(response.status_code)
            )
            response_data = response.data['results']
            if len(response_data) == 0:
                pass
            self.assertGreaterEqual(len(response_data), 0, 'Not found record in response')
            for product in response_data:
                result_found_in_string = f'{product["title"]} {product["description"]}'
                result_found_in_string = ''.join(transliterate(result_found_in_string))
                self.assertIn(
                    search_string,
                    result_found_in_string,
                    f'String {search_string} not found in product.title'
                )

    def _generate_search_data(self, items, field_name):
        field_value = self._get_random_field_value(items, field_name)
        return self._generate_random_substring(field_value)

    def _get_random_field_value(self, items, field_name):
        field_value = ''
        while len(field_value) < MIN_SEARCH_STRING_LENGTH:
            item = items[randint(0, len(items) - 1)]
            field_value = getattr(item, field_name, '')
        return field_value

    def _generate_random_substring(self, string):
        random_begin = randint(0, len(string) - MIN_SEARCH_STRING_LENGTH)
        random_end = randint(random_begin + MIN_SEARCH_STRING_LENGTH, len(string))
        return string[random_begin:random_end]
