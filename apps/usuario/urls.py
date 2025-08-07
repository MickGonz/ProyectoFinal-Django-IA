from django.urls import path
from .views import RegistroUsuarioCreateView, LoginUsuarioView, LogoutUsuarioView

app_name = 'apps.usuario'

urlpatterns = [
    path('registrar/', RegistroUsuarioCreateView.as_view(), name='registrar'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
]