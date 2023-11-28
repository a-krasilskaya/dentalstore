from django.db.models import F, Q
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .forms import ProductsFilterForm


from cart.forms import CartAddProductForm
from catalog.models import ProductCategory, Product, Gallery, TagProduct, Manufacturer


class CategoryListView(ListView):
    model = ProductCategory
    template_name = "catalog/catalog.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    allow_empty = False


    def get_queryset(self):
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        # фильтруем продкуты по слагу категории
        queryset = Product.objects.all().filter(category__slug=self.category.slug, publish=True)

        # если есть подкатегории - находим, проходим циклом по каждой, фильтруем по слагу подкатегории и объединяем с queryset
        # if self.category.get_descendants():
        #     for i in self.category.get_descendants():
        #         queryset = queryset.union(Product.objects.filter(category__slug=i.slug, publish=True))

        if self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=self.request.GET.get('min_price'))
        if self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=self.request.GET.get('max_price'))
        if self.request.GET.getlist('manufacturer'):
            queryset = queryset.filter(manufacturer__in=self.request.GET.get('manufacturer'))
        if self.request.GET.getlist('countries'):
            queryset = queryset.filter(manufacturer_countries__contains=self.request.GET.get('countries'))

        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['sub_categories'] = self.category.get_descendants()
        context['title'] = self.category
        context['parent'] = self.category.parent
        context['images'] = Gallery.objects.all()
        context['cat_level'] = self.category.get_level()
        context['cat_family'] = self.category.get_family()
        context['cat_siblings'] = self.category.get_siblings()
        context['cart_product_form'] = CartAddProductForm()
        context['form'] = ProductsFilterForm(self.request.GET)
        context['product_tags'] = TagProduct.objects.all().product_set.all()
            # ProductCategory.objects.get(slug=self.kwargs['slug']).tagproduct_set.all()
        # context['product_tags'] = Product.objects.filter(category__slug=self.category.slug, publish=True, tags__tag__isnull=False).values('tags__tag', 'tags__slug').distinct()

        # print(context['product_tags'].distinct())
        # context['product_tags'] = TagProduct.objects.all().filter(product_set=self.category)
        return context


class ProductTagView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'


    def get_queryset(self):
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        return Product.objects.all().filter(tags__slug=self.tag.slug, publish=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['title'] = self.category
        context['tag'] = self.tag
        context['list_prod'] = Product.objects.filter(tags__slug='tag_slug')
        context['product_tags'] = TagProduct.objects.all()
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








