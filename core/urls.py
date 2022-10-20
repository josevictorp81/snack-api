from django.urls import path

from . import views

urlpatterns = [
    path('classes/list', views.ClassesListAPIView.as_view(), name='list-class'),
]