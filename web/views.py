from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# from braces.views import SuperuserRequiredMixin

from core.models import Order, Snack, Classes

class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'


class StudentListView(TemplateView):
    template_name = 'student_list.html'


class SnackListView(ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack


class ClassListView(ListView):
    context_object_name = 'class_list'
    model = Classes
    template_name = 'class_list.html'
