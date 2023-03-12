from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='list-order'),
    path('new', views.OrderCreateAPIView.as_view(), name='create-order'),
    path('<int:pk>/update', views.OrderUpdateAPIView.as_view(), name='update-order'),
    path('<int:pk>/delete', views.OrderDeleteAPIView.as_view(), name='delete-order'),
]