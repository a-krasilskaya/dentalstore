from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='catalog'),
    path('<str:slug>/', views.ProductCategoryView.as_view(), name='product_category'),
    path('<str:slug>/<slug:tag_slug>/', views.ProductTagView.as_view(), name='product_tag'),
    path('<str:slug>/products/<str:product_slug>/', views.ShowProduct.as_view(), name='product_card'),
    path('products/paginations', views.ProductListAPIView.as_view(), name='paginations')
]