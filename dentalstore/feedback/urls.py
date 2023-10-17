from django.urls import path
from . import views
from .views import OrderCallBackFormView, FeedBackFormView

urlpatterns = [
    path('', OrderCallBackFormView.as_view(), name='ordercallback_view'),
    path('feedback-form', FeedBackFormView.as_view(), name='feedback_view')
]