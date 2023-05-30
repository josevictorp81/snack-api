from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib import messages
# from braces.views import SuperuserRequiredMixin

from core.models import Snack
from web.utils.snacks import ValidateSnacks


class SnackListView(ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack
    paginate_by = 25


class SnackCreateView(CreateView):
    model = Snack
    template_name = 'snack_form.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        name: str = request.POST['name']
        price: float = float(request.POST['price'])
        status: str = request.POST['available']

        if ValidateSnacks(request, name=name).validate_name():
            return redirect('create-snack')
        if ValidateSnacks(request, price=price).validate_price():
            return redirect('create-snack')

        available: bool = True if status == 'true' else False

        try:
            self.model.objects.create(
                name=name.title(), price=price, available=available)
            messages.add_message(request, messages.SUCCESS,
                                 'Lanche cadastrado com sucesso!')
            return redirect('snack-list-view')
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('create-snack')
