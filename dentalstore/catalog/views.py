from django.db.models import F, Q
from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cart.views import cart_add
from .forms import ProductsFilterForm
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.serializers import ProductSerializer, ManufacturerSerializer, ManufacturerValueSerializer, \
    ManufacturerCountriesSerializer
from rest_framework.exceptions import ValidationError

from cart.forms import CartAddProductForm
from catalog.models import ProductCategory, Product, Gallery, TagProduct, Manufacturer, Currency


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
    queryset = Product.objects.filter(id=0)

    # allow_empty = True

    # def get_queryset(self):
    #     self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
    #     queryset = Product.objects.all().filter(category__slug=self.category.slug, publish=True)
    #
    #     if self.request.GET.get('min_price'):
    #         queryset = queryset.filter(price__gte=self.request.GET.get('min_price'))
    #     if self.request.GET.get('max_price'):
    #         queryset = queryset.filter(price__lte=self.request.GET.get('max_price'))
    #     if self.request.GET.get('ordering'):
    #         queryset = queryset.order_by(self.request.GET.get('ordering'))
    #     if self.request.GET.getlist('manufacturer'):
    #         queryset = queryset.filter(manufacturer__name__in=self.request.GET.getlist('manufacturer'))
    #     if self.request.GET.getlist('countries'):
    #         queryset = queryset.filter(manufacturer_countries__in=self.request.GET.getlist('countries'))
    #     return queryset

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
        # products = Product.objects.filter(category__slug=self.category.slug, publish=True, tags__tag__isnull=False).values('tags__tag', 'tags__slug')
        # context['product_tags'] = [dict(s) for s in set(frozenset(d.items()) for d in products)]
        context['product_tags'] = Product.objects.filter(category__slug=self.category.slug, publish=True,
                                                         tags__tag__isnull=False).values('tags__tag', 'tags__slug',
                                                                                         'tags__parent',
                                                                                         'tags__parent__tag',
                                                                                         'tags__parent__slug',
                                                                                         'tags__id').order_by(
            'tags__tag', 'tags__parent__tag').distinct('tags__tag', 'tags__parent__tag')
        context['products_manufacturers'] = Product.objects.filter(category__slug=self.category.slug,
                                                                   publish=True).values('manufacturer__name').order_by(
            'manufacturer__name').distinct('manufacturer__name')
        context['products_manufacturer_countries'] = Product.objects.filter(category__slug=self.category.slug,
                                                                            publish=True).values(
            'manufacturer_countries').order_by(
            'manufacturer_countries').distinct('manufacturer_countries')
        return context


class ManufacturerListAPIView(generics.ListAPIView):
    model = Manufacturer
    serializer_class = ManufacturerValueSerializer

    def get_queryset(self):
        manufacturers = Product.objects.filter(
            category__slug=self.request.query_params.get('category')
        ).order_by('manufacturer').values_list('manufacturer__name').distinct()
        return [{'name': name} for name in manufacturers]


class CountriesListAPIView(generics.ListAPIView):
    serializer_class = ManufacturerCountriesSerializer
    def get_queryset(self):
        manufacturers_countries = Product.objects.filter(
            category__slug=self.request.query_params.get('category')
        ).order_by('manufacturer_countries').values_list('manufacturer_countries').distinct()
        return [{'manufacturer_countries': country} for country in manufacturers_countries]



class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        category_slug = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        ordering = self.request.query_params.get('ordering')
        manufacturers = self.request.query_params.get('manufacturers')
        countries = self.request.query_params.get('countries')

        if min_price:
            queryset = queryset.filter(price__gte=int(min_price), publish=True)
        if max_price:
            queryset = queryset.filter(price__lte=int(max_price), publish=True)
        if ordering:
            queryset = queryset.order_by(ordering)
        if manufacturers:
            queryset = queryset.filter(manufacturer__name__in=manufacturers.split(','))
        if countries:
            queryset = queryset.filter(manufacturer_countries__in=countries.split(','))
        if category_slug:
            try:
                category = ProductCategory.objects.get(slug=category_slug)
                queryset = queryset.filter(category__slug=category.slug, publish=True)
            except ProductCategory.DoesNotExist:
                raise ValidationError("Такой категории не существует")
        return queryset


class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        cart_add(request, product_id)
        return Response({"message": "Товар успешно добавлен в корзину"}, status=status.HTTP_200_OK)


class ProductTagView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'

    def get_queryset(self):
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        queryset = Product.objects.all().filter(tags__slug=self.tag.slug, publish=True)

        if self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=self.request.GET.get('min_price'))
        if self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=self.request.GET.get('max_price'))
        if self.request.GET.get('ordering'):
            queryset = queryset.order_by(self.request.GET.get('ordering'))
        if self.request.GET.getlist('manufacturer'):
            queryset = queryset.filter(manufacturer__name__in=self.request.GET.getlist('manufacturer'))
        if self.request.GET.getlist('countries'):
            queryset = queryset.filter(manufacturer_countries__in=self.request.GET.getlist('countries'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['title'] = self.category
        context['tag'] = self.tag
        context['list_prod'] = Product.objects.filter(tags__slug='tag_slug')
        context['product_tags'] = TagProduct.objects.all()
        context['images'] = Gallery.objects.all()
        context['form'] = ProductsFilterForm(self.request.GET)
        context['product_tags'] = Product.objects.filter(category__slug=self.category.slug, publish=True,
                                                         tags__tag__isnull=False).values('tags__tag', 'tags__slug',
                                                                                         'tags__parent',
                                                                                         'tags__parent__tag',
                                                                                         'tags__parent__slug',
                                                                                         'tags__id').order_by(
            'tags__tag',
            'tags__parent__tag').distinct('tags__tag',
                                          'tags__parent__tag')
        context['products_manufacturers'] = Product.objects.filter(tags__slug=self.tag.slug, publish=True).values(
            'manufacturer__name').order_by('manufacturer__name').distinct('manufacturer__name')
        context['products_manufacturer_countries'] = Product.objects.filter(tags__slug=self.tag.slug,
                                                                            publish=True).values(
            'manufacturer_countries').order_by(
            'manufacturer_countries').distinct('manufacturer_countries')
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
