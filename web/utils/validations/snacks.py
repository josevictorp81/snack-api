from django.contrib import messages
from django.http import HttpRequest

from core.models import Snack


class ValidateSnacks:
    def __init__(self, request: HttpRequest, name: str = None, price: float = None) -> None:
        self.name = name
        self.price = price
        self.request = request

    def validate_name(self) -> bool:
        if len(self.name) < 4:
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Nome muito curto para o lanche!')
            return True

        if not self.name.replace(' ', '').isalpha():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Nome inválido!')
            return True

        return False

    def validate_name_exists(self) -> bool:
        if Snack.objects.filter(name=self.name.title()).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Lanche com este nome já existe!')
            return True

    def validate_price(self) -> bool:
        if self.price < 0:
            messages.add_message(self.request, messages.ERROR,
                                 'Falha no cadastro! Preço não pode ser negativo!')
            return True

        return False
