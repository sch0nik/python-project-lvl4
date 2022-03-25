from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django_filters.views import FilterView

from apps.task_app.filters import TaskFilter
from apps.task_app.forms import CreateTaskForm
from apps.task_app.models import Task
from task_manager.mixins import OperationUpdate, OperationDelete


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task/base_list_task.html'
    context_object_name = 'task_list'
    filterset_class = TaskFilter


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'task/base_create_task.html'
    success_url = reverse_lazy('tasks')
    form_class = CreateTaskForm
    success_message = _('Задача успешно создана')

    def form_valid(self, form):
        new = form.save(commit=False)
        new.autor = self.request.user
        new.save()
        return super().form_valid(form)


class UpdateTaskView(OperationUpdate):
    template_name = 'task/base_update_task.html'
    model = Task
    form_class = CreateTaskForm
    success_message = _('Задача успешно изменена')
    success_url = reverse_lazy('tasks')
    redirect_field_name = reverse_lazy('tasks')


class DeleteTaskView(OperationDelete):
    template_name = 'task/base_delete_task.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Задача успешно удалена')

    def form_valid(self, form):
        if self.get_object().autor != self.request.user:
            messages.error(self.request, _('Задачу может удалить только её автор'))
        else:
            super(DeleteTaskView, self).form_valid(form)
        return redirect(self.success_url)


class TaskView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'task/base_detail_task.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data()
        context['labels'] = self.get_object().labels.all()
        return context
