from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse
# from braces.views import SuperuserRequiredMixin

from child.utils import generate_code
from core.models import Child
from web.utils.get_classes import get_classes, search_classes
from web.utils.get_fathers import get_fathers, search_father
from web.utils.students import ValidateStudents


class StudentListView(ListView):
    template_name = 'student_list.html'
    context_object_name = 'student_list'
    model = Child
    paginate_by = 25


class StudentCreateView(CreateView):
    model = Child
    template_name = 'studant_form.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        fathers = get_fathers()
        classes = get_classes()

        context = {
            'fathers': fathers,
            'classes': classes
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        name: str = request.POST['name']
        class_id: int = int(request.POST['class'])
        father: int = int(request.POST['father'])

        if ValidateStudents(request, name, class_id, father).validate():
            return redirect('create-student')

        try:
            code: str = generate_code()
            self.model.objects.create(
                name=name, father=search_father(father), class_id=search_classes(class_id), code=code)
            messages.add_message(request, messages.SUCCESS,
                                 'Aluno cadastrado com sucesso!')
            return redirect('student-list-view')
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect('create-student')


class StudentUpdateView(UpdateView):
    model = Child
    template_name = 'studant_form.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_edit: Child = Child.objects.get(id=kwargs['pk'])
        fathers = get_fathers()
        classes = get_classes()

        context = {
            'fathers': fathers,
            'classes': classes,
            'student_edit': student_edit
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        student_edit: Child = Child.objects.get(id=kwargs['pk'])
        name: str = request.POST['name']
        class_id: int = int(request.POST['class'])
        father: int = int(request.POST['father'])

        if ValidateStudents(request, name, class_id, father).validate():
            return redirect(reverse('edit-student', args=[student_edit.id]))

        try:
            student_edit.name = name
            student_edit.father = search_father(id=father)
            student_edit.class_id = search_classes(id=class_id)
            student_edit.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Aluno atualizado com sucesso!')
            return redirect(reverse('edit-student', args=[student_edit.id]))
        except:
            messages.add_message(request, messages.ERROR,
                                 'Erro interno do sistema!')
            return redirect(reverse('edit-student', args=[student_edit.id]))


class StudentDeleteView(DeleteView):
    model = Child
    success_url = '/controller/students'

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.add_message(request, messages.SUCCESS,
                             'Aluno deletado com sucesso!')
        return super().delete(request, *args, **kwargs)
