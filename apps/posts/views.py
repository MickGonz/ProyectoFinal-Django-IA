from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-publicado')

        # Obtener el parámetro de categoría de la URL
        categoria_slug = self.request.GET.get('categoria', None)
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)

        # Obtener el parámetro de ordenamiento de la URL
        orden = self.request.GET.get('orden', None)
        if orden == 'antiguo':
            queryset = queryset.order_by('publicado')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_individual.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.filter(post=self.object).order_by('-fecha_creacion')
        context['form'] = ComentarioForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            comentario = form.save(commit=False)
            comentario.post = self.object
            comentario.autor = request.user
            comentario.save()
            return redirect('apps.posts:post_individual', pk=self.object.pk)
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

class CrearPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        form.instance.publicado_por = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')