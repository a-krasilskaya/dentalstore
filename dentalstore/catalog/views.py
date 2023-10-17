from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cart.forms import CartAddProductForm
from catalog.models import ProductCategory, Product, Gallery


class CategoryListView(ListView):
    model = ProductCategory
    template_name = "catalog/catalog.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PriductCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    allow_empty = False


    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'], publish=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['title'] = self.category
        context['images'] = Gallery.objects.all()
        return context


class ShowProduct(DetailView):
    model = Product
    template_name = 'catalog/product_card.html'
    slug_url_kwarg = 'product_slug'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Gallery.objects.filter(product_id=self.object.id)
        context['cart_product_form'] = CartAddProductForm()
        return context



# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug)
#     cart_product_form = CartAddProductForm()
#     return render(request, 'cart/detail.html', {'product': product,
#                                                 'cart_product_form': cart_product_form})


# class PostByCategoryView(ListView):
#     context_object_name = 'posts'
#     template_name = 'blog/post_list.html'

    # def get_queryset(self):
    #     self.category = Category.objects.get(slug=self.kwargs['slug'])
    #     queryset = Post.objects.filter(category=self.category)
    #     return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = self.category
    #     return context


# def get_category(request, slag):
#     slag_category = ProductCategory.objects.get(slag=slag)
#     context = {
#         'category': slag_category,
#         'categories': ProductCategory.objects.all()
#     }
#     return render(request, 'catalog/product_list.html', context)


