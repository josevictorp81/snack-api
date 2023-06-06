from django.http import HttpRequest
from django.contrib import messages

from core.models import Classes


class ValidateClasses:
    def __init__(self, request: HttpRequest, name: str) -> None:
        self.request = request
        self.name = name

    def validate_register_class(self) -> bool:
        if len(self.name) < 5:
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Nome muito curto para a turma!')
            return True

        if Classes.objects.filter(name=self.name.title()).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Turma com este nome já existe!')
            return True

        return False
