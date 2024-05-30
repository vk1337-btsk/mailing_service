from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from apps.clients.models import Clients
from apps.newsletters.forms import NewsletterForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from apps.newsletters.models import Newsletters
from django.urls import reverse, reverse_lazy

from apps.users.models import Users


class NewslettersListView(PermissionRequiredMixin, ListView):
    model = Newsletters
    template_name = 'newsletters/newsletters_list.html'
    extra_context = {'title': 'Рассылки'}
    login_url = reverse_lazy('users:login')
    permission_required = ('newsletters.view_newsletters',)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.has_perm('newsletters.view_all_newsletters'):
            return queryset
        else:
            queryset = queryset.filter(owner=user)
            return queryset


class NewsletterDetailView(PermissionRequiredMixin, DetailView):
    model = Newsletters
    template_name = 'newsletters/newsletter_detail.html'
    extra_context = {'title': 'Рассылка'}
    login_url = reverse_lazy('users:login')
    permission_required = ('newsletters.view_newsletters',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists() or object.owner == user:
            return object
        else:
            raise PermissionDenied


class NewsletterCreateView(PermissionRequiredMixin, CreateView):
    model = Newsletters
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    extra_context = {'title': 'Добавить рассылку'}
    login_url = reverse_lazy('users:login')
    permission_required = ('newsletters.add_newsletters',)

    def get_success_url(self):
        return reverse('newsletters:newsletter', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['owner'] = self.request.user
        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Clients.objects.filter(owner=self.request.user)
        return form


class NewsletterUpdateView(PermissionRequiredMixin, UpdateView):
    model = Newsletters
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    extra_context = {'title': 'Изменить рассылку'}
    login_url = reverse_lazy('users:login')
    permission_required = ('newsletters.change_newsletters',)

    def get_success_url(self):
        return reverse('newsletters:newsletter', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['owner'] = self.request.user
        return data

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied


class NewsletterDeleteView(PermissionRequiredMixin, DeleteView):
    model = Newsletters
    template_name = 'newsletters/newsletter_confirm_delete.html'
    extra_context = {'title': 'Удалить рассылку'}
    success_url = reverse_lazy('newsletters:newsletters_list')
    login_url = reverse_lazy('users:login')
    permission_required = ('newsletters.delete_newsletters', 'newsletters.change_newsletters',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied


def set_newsletters_status(request, pk):
    """Контроллер изменения статуса рассылки"""
    if request.user.is_superuser or request.user.groups.filter(name='manager').exists():
        newsletter = Newsletters.objects.get(pk=pk)
        newsletter.is_active = not newsletter.is_active
        newsletter.save()
        return redirect(reverse('newsletters:newsletter', kwargs={'pk': newsletter.pk}))
