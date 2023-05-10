from django.views.generic import ListView
# from braces.views import SuperuserRequiredMixin

from core.models import Order, Snack, Classes, Child


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'


class StudentListView(ListView):
    template_name = 'student_list.html'
    context_object_name = 'student_list'
    model = Child


class SnackListView(ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack


class ClassListView(ListView):
    context_object_name = 'class_list'
    model = Classes
    template_name = 'class_list.html'
