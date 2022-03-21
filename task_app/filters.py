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

    labels = django_filters.ModelChoiceFilter(
        label=_('Метки'),
        field_name='labels',
        queryset=Label.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            'status',
            'executor',
            'labels',
            'my_task',
        )

    def my_task_filter(self, queryset, name, value):
        return queryset.filter(autor=self.request.user) if value else queryset
