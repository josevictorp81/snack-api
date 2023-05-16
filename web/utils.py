from django.http import HttpRequest
from django.contrib import messages
import re

from core.models import Classes


def validate_register_class(request: HttpRequest, name: str) -> bool:
    if len(name) < 5:
        messages.add_message(request, messages.ERROR,
                             'Nome muito curto para a turma!')
        return True

    res = re.search('^[0-9]+[a-zA-Z]*', name)
    if res is not None:
        messages.add_message(request, messages.ERROR, 'Nome inválido!')
        return True

    if Classes.objects.filter(name=name).exists():
        messages.add_message(request, messages.ERROR,
                             'Turma com este nome já existe!')
        return True

    return False
