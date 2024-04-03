from django.views.generic import ListView
from typing import Tuple

from catalog.forms import ProductsFilterForm
from catalog.models import ProductCategory, Gallery, Product


class ProductListMixins(ListView):
    model = Product
    template_name = 'catalog/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['title'] = self.category
        context['images'] = Gallery.objects.all()
        context['form'] = ProductsFilterForm(self.request.GET)

        return context


def transliterate(search_string: str) -> Tuple[str, str]:
    lower_string = search_string.lower()
    ru_to_eng = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ь': '',
        'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_'
    }

    eng_to_ru = {v: k for k, v in ru_to_eng.items()}
    eng_to_ru['e'] = 'е'

    eng = "".join(ru_to_eng.get(i, i) for i in lower_string)
    ru = "".join(eng_to_ru.get(i, i) for i in lower_string)

    return eng, ru

