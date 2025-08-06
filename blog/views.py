from django.shortcuts import render
from apps.posts.models import Post

def index(request):
    latest_posts = Post.objects.all().order_by('-publicado')[:3]
    context = {
        'latest_posts': latest_posts
    }
    return render(request, 'index.html', context)