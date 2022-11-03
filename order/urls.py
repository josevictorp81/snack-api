from django.urls import path

from . import views

urlpatterns = [
    path('list', views.OrderListAPIView.as_view(), name='list-order'),
    path('create', views.OrderCreateAPIView.as_view(), name='create-order'),
]