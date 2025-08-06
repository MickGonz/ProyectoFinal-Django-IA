from django.urls import path
from .views import ContactoCreateView

app_name = 'apps.contacto'

urlpatterns = [
    path('', ContactoCreateView.as_view(), name='contacto'),
]