from django.urls import path

from . import views

urlpatterns = [
    path('classes', views.ClassesListAPIView.as_view(), name='list-class'),
    path('snacks', views.SnackListAPIView.as_view(), name='list-snack'),
]