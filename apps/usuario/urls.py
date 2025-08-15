from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegistroView, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'apps.usuario'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registrar'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)