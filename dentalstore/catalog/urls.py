from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='catalog'),
    path('<str:slug>/', views.PriductCategoryView.as_view(), name='product_category'),
    path('<str:slug>/<str:product_slug>/', views.ShowProduct.as_view(), name='product_card'),
]