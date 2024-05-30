from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView

from django.urls import reverse, reverse_lazy
from apps.clients.forms import ClientForm, AddClientsToNewsletterForm
from apps.clients.models import Clients


class ClientsListView(PermissionRequiredMixin, ListView):
    model = Clients
    template_name = 'clients/clients_list.html'
    extra_context = {'title': 'Клиенты'}
    login_url = reverse_lazy('users:login')
    permission_required = ('clients.view_clients',)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.has_perm('clients.view_all_clients'):
            return queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(PermissionRequiredMixin, DetailView):
    model = Clients
    template_name = 'clients/client_detail.html'
    extra_context = {'title': 'Клиент'}
    login_url = reverse_lazy('users:login')
    permission_required = ('clients.view_clients',)

    def get_object(self, *args, **kwargs):
        object = super().get_object()
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists() or object.owner == user:
            return object
        else:
            raise PermissionDenied


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Clients
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    extra_context = {'title': 'Создать клиента'}
    login_url = reverse_lazy('users:login')
    permission_required = ('clients.add_clients',)

    def get_success_url(self):
        return reverse('clients:client', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Clients
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    extra_context = {'title': 'Редактировать клиента'}
    login_url = reverse_lazy('users:login')
    permission_required = ('clients.change_clients',)

    def get_success_url(self):
        return reverse('clients:client', kwargs={'pk': self.object.pk})

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Clients
    template_name = 'clients/client_confirm_delete.html'
    extra_context = {'title': 'Удалить клиента'}
    success_url = reverse_lazy('clients:clients_list')
    login_url = reverse_lazy('users:login')
    permission_required = ('clients.delete_clients', 'clients.change_clients',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied


class AddClientsToNewsletterView(PermissionRequiredMixin, FormView):
    template_name = 'clients/add_clients.html'
    form_class = AddClientsToNewsletterForm
    success_url = reverse_lazy('newsletters:newsletters_list')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)
