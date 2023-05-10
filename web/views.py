from django.views.generic import ListView
# from braces.views import SuperuserRequiredMixin

from core.models import Order, Snack, Classes, Child


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order_list.html'
    paginate_by = 15


class StudentListView(ListView):
    template_name = 'student_list.html'
    context_object_name = 'student_list'
    model = Child
    paginate_by = 25


class SnackListView(ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack
    paginate_by = 25


class ClassListView(ListView):
    context_object_name = 'class_list'
    model = Classes
    template_name = 'class_list.html'
    paginate_by = 25
