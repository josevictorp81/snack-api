from django.urls import path

from . import views

urlpatterns = [
    path('list', views.ChildListAPIView.as_view(), name='list-child'),
    path('create', views.ChildCreateAPIView.as_view(), name='create-child'),
]