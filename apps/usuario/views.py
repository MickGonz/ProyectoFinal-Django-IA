from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView # Asegúrate de que esto esté importado
from .forms import RegistroUsuarioForm, LoginForm

class RegistroUsuarioCreateView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registration/registrar.html'
    success_url = reverse_lazy('apps.usuario:login')

class LoginUsuarioView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    next_page = 'index'

class LogoutUsuarioView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = 'index'