from django.db.models import F, Q
from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cart.views import cart_add
from .forms import ProductsFilterForm
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.serializers import ProductSerializer, ManufacturerSerializer, ManufacturerValueSerializer, \
    ManufacturerCountriesSerializer
from rest_framework.exceptions import ValidationError

from cart.forms import CartAddProductForm
from catalog.models import ProductCategory, Product, Gallery, TagProduct, Manufacturer, Currency
from .utils import ProductListMixins


class CategoryListView(ListView):
    model = ProductCategory
    template_name = "catalog/catalog.html"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCategoryView(ProductListMixins, ListView):
    queryset = Product.objects.filter(id=0)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_tags'] = Product.objects.filter(category__slug=self.category.slug, publish=True,
                                                         tags__tag__isnull=False).values('tags__tag', 'tags__slug',
                                                                                         'tags__parent',
                                                                                         'tags__parent__tag',
                                                                                         'tags__parent__slug',
                                                                                         'tags__id').order_by(
            'tags__tag', 'tags__parent__tag').distinct('tags__tag', 'tags__parent__tag')
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
        tag_slug = self.request.query_params.get('tags')

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
        if tag_slug:
            try:
                tag = TagProduct.objects.get(slug=tag_slug)
                queryset = Product.objects.filter(tags__slug=tag.slug, publish=True)
            except TagProduct.DoesNotExist:
                raise ValidationError("Такой подкатегории не существует")

        return queryset


class AddToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        cart_add(request, product_id)
        return Response({"message": "Товар успешно добавлен в корзину"}, status=status.HTTP_200_OK)


class ProductTagView(ProductListMixins, ListView):
    queryset = Product.objects.filter(id=0)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.tag = TagProduct.objects.get(slug=self.kwargs['tag_slug'])
        self.category = ProductCategory.objects.get(slug=self.kwargs['slug'])
        context['tag'] = self.tag
        context['product_tags'] = Product.objects.filter(category__slug=self.category.slug, publish=True,
                                                         tags__tag__isnull=False).values('tags__tag', 'tags__slug',
                                                                                         'tags__parent',
                                                                                         'tags__parent__tag',
                                                                                         'tags__parent__slug',
                                                                                         'tags__id').order_by(
            'tags__tag',
            'tags__parent__tag').distinct('tags__tag',
                                          'tags__parent__tag')

        return context


class ManufacturerItemPage(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    queryset = Product.objects.filter(id=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.manufacturer = Manufacturer.objects.get(slug=self.kwargs['manufacturer_slug'])
        context['manufacturer'] = self.manufacturer
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
