from django.urls import path

from .views import classes, orders, students, snacks

urlpatterns = [
    path('orders', orders.OrderListView.as_view(), name='order-list-view'),
    path('students', students.StudentListView.as_view(), name='student-list-view'),
    path('snacks', snacks.SnackListView.as_view(), name='snack-list-view'),
    # classes
    path('classes', classes.ClassListView.as_view(), name='class-list-view'),
    path('classes/create', classes.ClassCreateView.as_view(), name='create-class'),
    path('classes/<int:pk>/update',
         classes.ClassUpdateView.as_view(), name='edit-class'),
    path('classes/<int:pk>/delete',
         classes.ClassDeleteView.as_view(), name='delete-class'),
]
