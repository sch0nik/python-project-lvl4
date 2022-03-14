import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from fourth.task_manager.models import Task


class TaskFilter(django_filters.FilterSet):
    my_task = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='my_task_filter',
        widget=forms.CheckboxInput,
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
        if value:
            return queryset & self.request.user.task.all()
        return queryset
