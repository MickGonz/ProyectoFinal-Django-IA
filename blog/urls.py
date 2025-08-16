from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, acerca_de # Importa las vistas necesarias

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('posts/', include('apps.posts.urls')),
    path('contacto/', include('apps.contacto.urls')),
    path('usuario/', include('apps.usuario.urls')),
    path('acerca-de/', acerca_de, name='acerca_de'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)