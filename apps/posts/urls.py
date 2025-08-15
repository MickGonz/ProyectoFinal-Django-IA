from django.urls import path
from .views import PostListView, PostDetailView, CrearPostView, PostUpdateView, PostDeleteView

app_name = 'apps.posts'

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_individual'),
    path('crear/', CrearPostView.as_view(), name='crear_post'),
    path('<int:pk>/editar/', PostUpdateView.as_view(), name='editar_post'),
    path('<int:pk>/eliminar/', PostDeleteView.as_view(), name='eliminar_post'),
]