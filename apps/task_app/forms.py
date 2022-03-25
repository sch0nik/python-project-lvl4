from django import forms

from apps.task_app.models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'executor',
            'status',
            'labels',
        )
