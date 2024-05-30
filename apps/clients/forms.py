from django import forms

from apps.clients.models import Clients
from apps.newsletters.models import Newsletters
from core.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('owner',)


class AddClientsToNewsletterForm(forms.Form):

    newsletter = forms.ModelChoiceField(queryset=Newsletters.objects.all(), label='Рассылка')
    clients = forms.ModelMultipleChoiceField(queryset=Clients.objects.all(), label='Клиенты',
                                             widget=forms.CheckboxSelectMultiple)
