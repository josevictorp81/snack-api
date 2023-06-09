from django.urls import path

from .views import classes, orders, students, snacks, authentication

urlpatterns = [
    # authentication
    path('login', authentication.AuthLoginView.as_view(), name='login'),
    path('logout', authentication.AuthLogoutView.as_view(), name='logout'),

    # orders
    path('orders', orders.OrderListView.as_view(), name='order-list'),
    path('orders/create', orders.OrderCreateView.as_view(), name='create-order'),
    path('orders/<int:pk>/update',
         orders.OrderUpdateView.as_view(), name='edit-order'),
    path('orders/<int:pk>/delete',
         orders.OrderDeleteView.as_view(), name='delete-order'),

    # students
    path('students', students.StudentListView.as_view(), name='student-list'),
    path('students/create', students.StudentCreateView.as_view(),
         name='create-student'),
    path('students/<int:pk>/update', students.StudentUpdateView.as_view(),
         name='edit-student'),
    path('students/<int:pk>/delete', students.StudentDeleteView.as_view(),
         name='delete-student'),

    # snacks
    path('snacks', snacks.SnackListView.as_view(), name='snack-list'),
    path('snacks/create', snacks.SnackCreateView.as_view(), name='create-snack'),
    path('snacks/<int:pk>/update',
         snacks.SnackUpdateView.as_view(), name='edit-snack'),
    path('snacks/<int:pk>/delete',
         snacks.SnackDeleteView.as_view(), name='delete-snack'),

    # classes
    path('classes', classes.ClassListView.as_view(), name='class-list'),
    path('classes/create', classes.ClassCreateView.as_view(), name='create-class'),
    path('classes/<int:pk>/update',
         classes.ClassUpdateView.as_view(), name='edit-class'),
    path('classes/<int:pk>/delete',
         classes.ClassDeleteView.as_view(), name='delete-class'),
]
