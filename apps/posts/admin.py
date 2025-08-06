from django.contrib import admin
from .models import Categoria, Post

# Clases para personalizar la vista en el admin
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'subtitulo', 'fecha', 'activo', 'categoria', 'imagen', 'publicado')

# Registra tus modelos aquí.
admin.site.register(Categoria)
admin.site.register(Post, PostAdmin)