from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrderListView.as_view(), name='order-list-view'),
    path('students', views.StudentListView.as_view(), name='student-list-view'),
    path('snacks', views.SnackListView.as_view(), name='snack-list-view'),
    path('classes', views.ClassListView.as_view(), name='class-list-view'),

    path('classes/create', views.ClassCreateView.as_view(), name='create-class'),
    path('classes/<int:id>/edit', views.ClassUpdateView.as_view(), name='edit-class'),
]
