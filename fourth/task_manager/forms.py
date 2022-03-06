from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = _(
            'Ваш пароль должен содержать как минимум 3 символа.',
        )

    first_name = forms.CharField(label=_('Имя'), max_length=150)
    last_name = forms.CharField(label=_('Фамилия'), max_length=150)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
