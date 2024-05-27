from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.

class Home(LoginRequiredMixin, TemplateView):
    template_name = "home/inicio.html"
    login_url=reverse_lazy('users_app:login')

class AuditViews(LoginRequiredMixin, TemplateView):
    template_name="administrador/auditorias/auditoriasindex.html"
    login_url=reverse_lazy('users_app:login')

class GenericsViews(LoginRequiredMixin, TemplateView):
    template_name="administrador/genericas/genericasindex.html"
    login_url=reverse_lazy('users_app:login')