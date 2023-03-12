from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChildListAPIView.as_view(), name='list-child'),
    path('new', views.ChildCreateAPIView.as_view(), name='create-child'),
]