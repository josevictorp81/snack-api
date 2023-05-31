from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
from django.contrib import messages
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
