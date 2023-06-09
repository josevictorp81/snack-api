from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import Snack
from web.utils.validations.snacks import ValidateSnacks


class SnackListView(LoginRequiredMixin, ListView):
    context_object_name = 'snack_list'
    template_name = 'snack_list.html'
    model = Snack
    paginate_by = 25
    login_url = 'login'


class SnackCreateView(LoginRequiredMixin, CreateView):
    model = Snack
    template_name = 'snack_form.html'
    login_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        name: str = request.POST['name']
        price: float = float(request.POST['price'])
        status: str = request.POST['available']

        if ValidateSnacks(request, name=name).validate_name_exists():
            return redirect('create-snack')
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
            return redirect('snack-list')
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('create-snack')


class SnackUpdateView(LoginRequiredMixin, UpdateView):
    model = Snack
    template_name = 'snack_form.html'
    login_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        snack_edit: Snack = self.model.objects.get(id=kwargs['pk'])

        context = {
            'snack_edit': snack_edit
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        snack_edit: Snack = self.model.objects.get(id=kwargs['pk'])
        name: str = request.POST['name']
        price: float = float(request.POST['price'])
        status: str = request.POST['available']

        available: bool = True if status == 'true' else False

        if ValidateSnacks(request, name=name).validate_name():
            return redirect(reverse('edit-snack', args=[snack_edit.id]))
        if ValidateSnacks(request, price=price).validate_price():
            return redirect(reverse('edit-snack', args=[snack_edit.id]))

        try:
            snack_edit.name = name
            snack_edit.price = price
            snack_edit.available = available
            snack_edit.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Lanche atualizado com sucesso!')
            return redirect(reverse('edit-snack', args=[snack_edit.id]))
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('edit-snack')


class SnackDeleteView(LoginRequiredMixin, DeleteView):
    model = Snack
    success_url = '/controller/snacks'
    login_url = 'login'

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Lanche excluído com sucesso!')
        return super().delete(request, *args, **kwargs)
