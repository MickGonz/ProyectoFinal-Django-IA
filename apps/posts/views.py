from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q 

class PostListView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-publicado')

        categoria_slug = self.request.GET.get('categoria', None)
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)

        orden = self.request.GET.get('orden', None)
        if orden == 'antiguo':
            queryset = queryset.order_by('publicado')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        # Esta línea obtiene los 3 posts más recientes
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_individual.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.filter(post=self.object).order_by('-fecha_creacion')
        context['form'] = ComentarioForm()
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
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

# Nueva vista para editar comentarios
class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    fields = ['contenido']
    template_name = 'posts/editar_comentario.html'

    def get_success_url(self):
        return reverse('apps.posts:post_individual', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.autor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context

# Nueva vista para eliminar comentarios
class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'posts/eliminar_comentario.html'

    def get_success_url(self):
        return reverse('apps.posts:post_individual', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.autor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context

class CrearPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        form.instance.publicado_por = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context
# Nueva vista para la búsqueda
class PostSearchView(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(titulo__icontains=query) | Q(subtitulo__icontains=query) | Q(texto__icontains=query)
            ).distinct()
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        # Aquí también se agregan los posts recientes
        context['ultimos_posts'] = Post.objects.all().order_by('-publicado')[:3] 
        return context