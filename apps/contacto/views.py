from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Contacto
from .forms import ContactoForm

class ContactoCreateView(CreateView):
    model = Contacto
    form_class = ContactoForm
    template_name = 'contacto/contacto.html'
    success_url = reverse_lazy('index')