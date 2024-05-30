from apps.clients.models import Clients
from apps.messages_.models import Messages
from apps.newsletters.models import Newsletters
from django import forms
from core.forms import StyleFormMixin


class NewsletterForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_newsletter'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].queryset = Messages.objects.filter(owner=owner)
        self.fields['clients'].queryset = Clients.objects.filter(owner=owner)

    class Meta:
        model = Newsletters
        exclude = ('owner', 'date_next_mailing')
