from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='catalog'),
    path('manufacturers/', views.ManufacturerListAPIView.as_view(), name='manufacturers'),
    path('manufacturers/countries/', views.CountriesListAPIView.as_view(), name='manufacturers_countries'),
    path('manufacturer/item/<str:manufacturer_slug>/', views.ManufacturerItemPage.as_view(), name='manufacturer'),
    path('<str:slug>/', views.ProductCategoryView.as_view(), name='product_category'),
    path('<str:slug>/<slug:tag_slug>/', views.ProductTagView.as_view(), name='product_tag'),
    path('<str:slug>/products/<str:product_slug>/', views.ShowProduct.as_view(), name='product_card'),
    path('manufacturer/item/<str:manufacturer_slug>/', views.ManufacturerItemPage.as_view(), name='manufacturer'),
    path(
        'manufacturer/item/<str:manufacturer_slug>/products/<str:product_slug>/',
        views.ShowProduct.as_view(),
        name='product_card',
    ),
    path('products/paginations', views.ProductListAPIView.as_view(), name='paginations'),
    path('add_to_cart/<int:id>/append/', views.AddToCartAPIView.as_view(), name='add_to_cart'),
]
