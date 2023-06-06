from datetime import date
from django.http import HttpRequest
from django.contrib import messages

from core.models import Child, Order


class ValidateOrders:
    def __init__(self, request: HttpRequest, student: int, date: date) -> None:
        self.request = request
        self.student = student
        self.date = date

    def validate(self) -> bool:
        if not Child.objects.filter(id=self.student).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Erro no cadastro! Aluno não existe!')
            return True

        if self.date < date.today():
            messages.add_message(self.request, messages.ERROR,
                                 'Erro no cadastro! Não é possível fazer um pedidos para um dia anterior!')
            return True

        if Order.objects.filter(child_id=self.student, date=self.date).exists():
            messages.add_message(self.request, messages.ERROR,
                                 'Erro no cadastro! Já existe um pedido para este dia!')
            return True

        return False


def str_to_date(date_str: str) -> date:
    date_conv = date_str.split('-')
    return date(int(date_conv[0]), int(date_conv[1]), int(date_conv[2]))
