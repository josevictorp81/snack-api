from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
from django.contrib import messages
# from braces.views import SuperuserRequiredMixin

from core.models import Order
from web.utils.get_students import get_students, search_student
from web.utils.get_snacks import get_snacks, search_snack
from web.utils.orders import ValidateOrders, str_to_date


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order_list.html'
    paginate_by = 15


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_form.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            'students': get_students(),
            'snacks': get_snacks()
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student: str = request.POST['child']
        date_str: str = request.POST['date']
        snack: list = request.POST.getlist('snack')

        order_date = str_to_date(date_str)

        if ValidateOrders(request, student, order_date).validate():
            return redirect('create-order')

        try:
            order_value: float = 0
            student = search_student(id=int(student))
            order = self.model.objects.create(
                date=order_date, child_id=student)
            for i in snack:
                sn = search_snack(id=int(i))
                order_value += sn.price
                order.snack_id.add(sn)

            order.order_value = order_value
            order.save()
            order_value = 0
            messages.add_message(request, messages.SUCCESS,
                                 'Pedido cadastrado com sucesso!')
            return redirect('order-list-view')

        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('create-order')
