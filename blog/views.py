"""Blog app views."""
from django.views.generic import ListView, DetailView
from .models import Post, CategoriaBlog, TagBlog


class PostListView(ListView):
    """List all published posts."""
    model = Post
    template_name = 'blog/lista.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status='publicado')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaBlog.objects.all()
        context['posts_destaque'] = Post.objects.filter(status='publicado', destaque=True)[:3]
        return context


class CategoriaPostListView(ListView):
    """List posts by category."""
    model = Post
    template_name = 'blog/lista.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            status='publicado',
            categoria__slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_atual'] = CategoriaBlog.objects.get(slug=self.kwargs['slug'])
        context['categorias'] = CategoriaBlog.objects.all()
        return context


class TagPostListView(ListView):
    """List posts by tag."""
    model = Post
    template_name = 'blog/lista.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            status='publicado',
            tags__slug=self.kwargs['slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_atual'] = TagBlog.objects.get(slug=self.kwargs['slug'])
        context['categorias'] = CategoriaBlog.objects.all()
        return context


class PostDetailView(DetailView):
    """Post detail page."""
    model = Post
    template_name = 'blog/detalhe.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Post.objects.filter(status='publicado')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.visualizacoes += 1
        obj.save(update_fields=['visualizacoes'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_relacionados'] = Post.objects.filter(
            status='publicado',
            categoria=self.object.categoria
        ).exclude(id=self.object.id)[:3]
        return context
