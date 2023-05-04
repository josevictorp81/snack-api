from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrderListView.as_view(), name='order-list-view'),
    path('students', views.StudentListView.as_view(), name='student-list-view'),
    path('snacks', views.SnackListView.as_view(), name='snack-list-view'),
    path('classes', views.ClassListView.as_view(), name='class-list-view'),
]
