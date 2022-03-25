from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.user_app.models import User


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = _(
            'Ваш пароль должен содержать как минимум 3 символа.',
        )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
