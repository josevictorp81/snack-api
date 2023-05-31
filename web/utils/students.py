from django.contrib import messages
from django.http import HttpRequest

from django.contrib.auth.models import User
from core.models import Classes


class ValidateStudents:
    def __init__(self, request: HttpRequest, name: str, class_id: int, father: int) -> None:
        self.request = request
        self.name = name
        self.class_id = class_id
        self.father = father

    def validate(self) -> bool:
        if not self.name.replace(' ', '').isalpha():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Nome inválido!')
            return True

        if not User.objects.filter(id=self.father).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Pai enexistente!')
            return True

        if not Classes.objects.filter(id=self.class_id).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Turma enexistente!')
            return True

        return False
