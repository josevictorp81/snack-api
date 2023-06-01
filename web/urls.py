from django.urls import path

from .views import classes, orders, students, snacks

urlpatterns = [
    path('orders', orders.OrderListView.as_view(), name='order-list-view'),
    # students
    path('students', students.StudentListView.as_view(), name='student-list-view'),
    path('students/create', students.StudentCreateView.as_view(),
         name='create-student'),
    path('students/<int:pk>/update', students.StudentUpdateView.as_view(),
         name='edit-student'),

    # snacks
    path('snacks', snacks.SnackListView.as_view(), name='snack-list-view'),
    path('snacks/create', snacks.SnackCreateView.as_view(), name='create-snack'),
    path('snacks/<int:pk>/update',
         snacks.SnackUpdateView.as_view(), name='edit-snack'),
    path('snacks/<int:pk>/delete',
         snacks.SnackDeleteView.as_view(), name='delete-snack'),

    # classes
    path('classes', classes.ClassListView.as_view(), name='class-list-view'),
    path('classes/create', classes.ClassCreateView.as_view(), name='create-class'),
    path('classes/<int:pk>/update',
         classes.ClassUpdateView.as_view(), name='edit-class'),
    path('classes/<int:pk>/delete',
         classes.ClassDeleteView.as_view(), name='delete-class'),
]
