from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from apps.messages_.forms import MessageForm
from apps.messages_.models import Messages


class MessagesListView(PermissionRequiredMixin, ListView):
    model = Messages
    template_name = 'messages/messages_list.html'
    login_url = reverse_lazy('users:login')
    permission_required = ('messages_.view_messages',)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.has_perm('messages_.view_all_messages'):
            return queryset
        else:
            queryset = queryset.filter(owner=user)
            return queryset


class MessageDetailView(PermissionRequiredMixin, DetailView):
    model = Messages
    template_name = 'messages/message_detail.html'
    extra_context = {'title': 'Сообщение'}
    login_url = reverse_lazy('users:login')
    permission_required = ('messages_.view_messages',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists() or object.owner == user:
            return object
        else:
            raise PermissionDenied


class MessageCreateView(PermissionRequiredMixin, CreateView):
    model = Messages
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    extra_context = {'title': 'Создание сообщения'}
    login_url = reverse_lazy('users:login')
    permission_required = ('messages_.add_messages',)

    def get_success_url(self):
        return reverse('messages_:message', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Messages
    form_class = MessageForm
    template_name = 'messages/message_form.html'
    extra_context = {'title': 'Редактирование сообщения'}
    login_url = reverse_lazy('users:login')
    permission_required = ('messages_.change_messages',)

    def get_success_url(self):
        return reverse('messages_:message', kwargs={'pk': self.object.pk})

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Messages
    template_name = 'messages/message_confirm_delete.html'
    extra_context = {'title': 'Подтверждение удаления'}
    success_url = reverse_lazy('messages_:messages_list')
    login_url = reverse_lazy('users:login')
    permission_required = ('messages_.delete_messages', 'messages_.change_messages',)

    def get_object(self, *args, **kwargs):
        object = super().get_object(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or object.owner == user:
            return object
        else:
            raise PermissionDenied
