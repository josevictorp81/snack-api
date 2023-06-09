from typing import Any
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse


class AuthLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('order-list')
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Usuário ou senha inválidos!')
            return redirect('login')
        if not user.is_superuser:
            messages.add_message(request, messages.ERROR,
                                 'Usuário sem permissão de acesso!')
            return redirect('login')
        else:
            login(request, user)
            return redirect('order-list')


class AuthLogoutView(LogoutView):
    next_page = 'login'
