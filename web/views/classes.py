from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import Classes
from web.utils.validations.classes import ValidateClasses


class ClassListView(LoginRequiredMixin, ListView):
    context_object_name = 'class_list'
    model = Classes
    template_name = 'class_list.html'
    paginate_by = 25
    login_url = 'login'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()


class ClassCreateView(LoginRequiredMixin, CreateView):
    template_name = 'class_form.html'
    model = Classes
    login_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        class_name = request.POST['name']

        if ValidateClasses(request, class_name).validate_register_class():
            return redirect('create-class')

        try:
            self.model.objects.create(name=class_name.title())
            messages.add_message(request, messages.SUCCESS,
                                 'Turma cadastrada com sucesso!')
            return redirect('class-list')
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('create-class')


class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Classes
    template_name = 'class_form.html'
    login_url = 'login'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        class_edit: Classes = self.model.objects.get(id=kwargs['pk'])

        context = {
            'class_edit': class_edit
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        class_edit: Classes = self.model.objects.get(id=kwargs['pk'])

        try:
            class_edit.name = self.request.POST['name']
            class_edit.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Turma atualizada com sucesso!')
            return redirect(reverse('edit-class', args=[class_edit.id]))
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect(reverse('edit-class', args=[class_edit.id]))


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Classes
    success_url = '/controller/classes'
    login_url = 'login'

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Turma excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
