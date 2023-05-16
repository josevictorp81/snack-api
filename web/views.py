from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
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


class ClassCreateView(CreateView):
    template_name = 'class_form.html'
    model = Classes

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        class_name = request.POST['name']

        try:
            self.model.objects.create(name=class_name)
            return redirect('create-class')
        except:
            print('erro')
