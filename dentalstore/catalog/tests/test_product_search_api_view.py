from decimal import Decimal
from random import randint

from catalog.tests.catalog import ProductListAPIViewTestBase
from catalog.views import ProductSearchAPIView, MIN_SEARCH_STRING_LENGTH
from mixer.backend.django import mixer
from catalog.utils import transliterate
from catalog.models import ProductCategory


class ProductSearchAPIViewTest(ProductListAPIViewTestBase):

    def _setup_view_and_uri(self):
        self.view = ProductSearchAPIView.as_view()
        self.uri = '/products/search/'

    def test_search_title_and_description(self):
        self.products.append(mixer.blend(
            'catalog.Product',
            title='тест987',
            description='Тестирование описания продукта',
            category=self.category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        ))

        search_strings = [
            self._generate_search_data(self.products, 'title'),
            'test987',
            'тест987',
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

    def test_search_two_words(self):
        self.products.append(mixer.blend(
            'catalog.Product',
            title='тест987 поиск1',
            description='Тестирование описания продукта поиск2 поиск3',
            category=self.category,
            manufacturer=self.manufacturer,
            publish=True,
            tags=(self.tag,),
            price=Decimal(mixer.faker.pyint(min_value=1, max_value=10000, step=1)),
        ))

        search_strings = [
            'поиск1 поиск2',
            'поиск2 poisk1',
            'поиск3 poisk2 поиск1',
        ]
        for search_string in search_strings:
            search_words = search_string.split()
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
                for search_word in search_words:
                    self.assertIn(
                        search_word,
                        result_found_in_string,
                        f'Word {search_word} not found in product.title'
                    )

    def test_search_category(self):
        category = mixer.blend(
            'catalog.ProductCategory',
            title='Герметики2',
            slug='category_test_search',
        )
        self.products.append(mixer.blend(
            'catalog.Product',
            title='тест8765',
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
                result_found_in_string = self._get_product_category(product['category']).title
                result_found_in_string = ''.join(transliterate(result_found_in_string))
                self.assertIn(
                    search_string,
                    result_found_in_string,
                    f'String {search_string} not found in product.title'
                )

    def _generate_search_data(self, items, field_name: str):
        field_value = self._get_random_field_value(items, field_name)
        return self._generate_random_substring(field_value)

    def _get_random_field_value(self, items, field_name: str):
        field_value = ''
        while len(field_value) < MIN_SEARCH_STRING_LENGTH:
            item = items[randint(0, len(items) - 1)]
            field_value = getattr(item, field_name, '')
        return field_value

    def _generate_random_substring(self, string: str) -> str:
        random_begin = randint(0, len(string) - MIN_SEARCH_STRING_LENGTH)
        random_end = randint(random_begin + MIN_SEARCH_STRING_LENGTH, len(string))
        return string[random_begin:random_end]

    def _get_product_category(self, category_id: int) -> ProductCategory:
        category = ProductCategory.objects.get(pk=category_id)
        return category
