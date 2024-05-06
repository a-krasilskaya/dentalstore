from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('delivery/', views.delivery, name='delivery'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('about/', views.about, name='about'),
    path('sertificate/', views.sertificate, name='sertificate'),
    path('image_to_pdf/<path:image_name>/', views.image_to_pdf, name='image_to_pdf'),
    path('list_images/', views.list_images, name='list_images'),
]