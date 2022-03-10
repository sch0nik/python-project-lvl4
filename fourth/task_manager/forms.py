from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from fourth.task_manager.models import StatusTask, Task, Label


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


class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = StatusTask
        fields = ('name',)


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name',)


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'executor',
            'status',
            'label',
        )
        labels = {
            'executor': _('Испольнитель'),
            'status': _('Статус'),
            'label': _('Метки'),
        }
