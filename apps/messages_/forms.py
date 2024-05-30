from django import forms
from core.forms import StyleFormMixin
from apps.messages_.models import Messages


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Messages
        exclude = ('owner',)
