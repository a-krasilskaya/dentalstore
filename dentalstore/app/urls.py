from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('delivery/', views.delivery, name='delivery'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]