from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.blog.forms import ArticleForm
from apps.blog.models import Articles
from django.urls import reverse, reverse_lazy

from apps.blog.utils import get_article_list_from_cache


class ArticlesListView(ListView):
    model = Articles
    template_name = 'blog/articles_list.html'
    extra_context = {'title': 'Новости'}

    def get_queryset(self):
        return get_article_list_from_cache()


class ArticlesDetailView(DetailView):
    model = Articles
    template_name = 'blog/article_detail.html'
    extra_context = {'title': 'Статья'}
    permission_required = ('blog.view_article',)

    def get_object(self, *args, **kwargs):
        self.object = super().get_object()
        self.object.views += 1
        self.object.save()
        return self.object


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {"title": "Создание статьи"}
    login_url = reverse_lazy('users:login')
    permission_required = ('blog.add_articles',)

    def get_success_url(self):
        return reverse('blog:article', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Articles
    template_name = 'blog/article_confirm_delete.html'
    extra_context = {"title": "Удаление статьи"}
    success_url = reverse_lazy('blog:articles_list')
    login_url = reverse_lazy('users:login')
    permission_required = ('blog.delete_articles', 'blog.change_articles',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or (user.groups.filter(name='content_manager').exists() and object.author == user):
            return object
        else:
            raise PermissionDenied


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Articles
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {"title": "Редактирование статьи"}
    login_url = reverse_lazy('users:login')
    permission_required = ('blog.change_articles',)

    def get_success_url(self):
        return reverse('blog:article', kwargs={'slug': self.object.slug})

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or (user.groups.filter(name='content_manager').exists() and object.author == user):
            return object
        else:
            raise PermissionDenied
