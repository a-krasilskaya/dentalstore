from django.views.generic import ListView

from cart.forms import CartAddProductForm
from catalog.forms import ProductsFilterForm
from catalog.models import ProductCategory, Gallery, Product
import sys

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




