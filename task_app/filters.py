import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_app.models import Task, Label, User


class TaskFilter(django_filters.FilterSet):
    my_task = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='my_task_filter',
        widget=forms.CheckboxInput,
    )

    executor = django_filters.ModelChoiceFilter(
        label=_('Исполнитель'),
        field_name='executor',
        queryset=User.objects.all(),
    )

    label = django_filters.ModelChoiceFilter(
        label=_('Метка'),
        field_name='label',
        queryset=Label.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            'status',
            'executor',
            'label',
            'my_task',
        )

    def my_task_filter(self, queryset, name, value):
        return queryset.filter(autor=self.request.user) if value else queryset
