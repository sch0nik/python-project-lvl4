import django_filters
from django.utils.translation import gettext_lazy as _

from fourth.task_manager.models import Task


class TaskFilter(django_filters.FilterSet):
    my_task = django_filters.BooleanFilter(label=_('Только свои задачи'))

    class Meta:
        model = Task
        fields = (
            'status',
            'executor',
            'label',
        )

    # def is_valid(self):
    #     if self.request.user
