from django.shortcuts import render
from django.views.generic import ListView, DetailView # Asegúrate de importar DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html' # El material sugiere mover este archivo a una subcarpeta 'posts'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_individual.html'
    context_object_name = 'post'