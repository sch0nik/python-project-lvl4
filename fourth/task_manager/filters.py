import django_filters
from django import forms
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from fourth.task_manager.models import Task, StatusTask, Label, User


class TaskFilter(django_filters.FilterSet):
    my_task = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='my_task_filter',
        widget=forms.CheckboxInput,
    )

    executor_filter = django_filters.ModelChoiceFilter(
        label=_('Исполнитель'),
        field_name='executor',
        queryset=User.objects.all(),
    )

    label_filter = django_filters.ModelChoiceFilter(
        label=_('Метка'),
        field_name='label',
        queryset=Label.objects.all(),
    )

    # TODO: поле executor должно быть представлено в виде full_name
    class Meta:
        model = Task
        fields = (
            'status',
            'executor_filter',
            'label_filter',
            'my_task',
        )

    def my_task_filter(self, queryset, name, value):
        return queryset.filter(autor=self.request.user) if value else queryset
