from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'apps.posts'

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_individual'),
]