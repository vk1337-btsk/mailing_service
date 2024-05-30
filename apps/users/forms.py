from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordResetForm
from django import forms
from core.forms import StyleFormMixin
from apps.users.models import Users


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'password1', 'password2', 'user_name', 'first_name', 'last_name', 'middle_name')


class LoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'phone', 'country', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class RecoveryForm(StyleFormMixin, PasswordResetForm):
    pass
