from django.urls import path

from . import views

urlpatterns =[
    path('signup', views.UserCreateAPIView.as_view(), name='signup-user'),
    path('profile', views.UserManagerAPIView.as_view(), name='profile-user'),
] 