from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django_filters.views import FilterView

from task_app.mixins import OperationList, OperationDelete, \
    OperationUpdate
from task_app.filters import TaskFilter
from task_app.forms import (
    CreateUserForm,
    CreateStatusForm,
    CreateTaskForm,
    CreateLabelForm,
)
from task_app.models import StatusTask, Task, Label, User


class IndexView(TemplateView):
    template_name = 'base_index.html'


class UsersView(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'users/base_list_user.html'
    context_object_name = 'users'


class CreateUserView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/base_create_user.html'
    success_url = reverse_lazy('login')
    form_class = CreateUserForm
    success_message = _('Пользователь успешно зарегистрирован')


class LoginUserView(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/base_login_user.html'
    next_page = reverse_lazy('index')
    success_message = _('Вы залогинены')
    success_url = reverse_lazy('index')


class LogoutUserView(SuccessMessageMixin, LogoutView):
    success_message = _('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, self.success_message)
        return redirect('index')


class UpdateUserView(OperationUpdate):
    model = User
    template_name = 'users/base_update_user.html'
    form_class = CreateUserForm
    success_message = _('Пользователь успешно изменён')
    redirect_field_name = reverse_lazy('login')


class DeleteUserView(OperationDelete):
    model = User
    template_name = 'users/base_delete_user.html'
    success_message = _('Пользователь успешно удалён')
    success_url = reverse_lazy('users')
    msg_error = _('У вас нет прав для изменения другого пользователя.')

    def form_valid(self, form):
        if self.get_object() != self.request.user:
            messages.error(self.request, self.msg_error)
        else:
            super(DeleteUserView, self).form_valid(form)
        return redirect(self.success_url)


class StatusesView(OperationList):
    template_name = 'status/base_list_status.html'
    queryset = StatusTask.objects.order_by('id')
    context_object_name = 'statuses'


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status/base_create_status.html'
    success_url = reverse_lazy('statuses')
    form_class = CreateStatusForm
    success_message = _('Статус успешно создан')


class UpdateStatusView(OperationUpdate):
    model = StatusTask
    template_name = 'status/base_update_status.html'
    form_class = CreateStatusForm
    success_message = _('Статус успешно изменён')
    success_url = reverse_lazy('statuses')
    redirect_field_name = reverse_lazy('statuses')


class DeleteStatusView(OperationDelete):
    model = StatusTask
    template_name = 'status/base_delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно удалён')
    msg_error = _('Невозможно удалить статус, потому что он используется')

    def form_valid(self, form):
        if self.get_object().task.all():
            messages.error(self.request, self.msg_error)
        else:
            super(DeleteStatusView, self).form_valid(form)
        return redirect(self.success_url)


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


class LabelsView(OperationList):
    template_name = 'label/base_list_label.html'
    queryset = Label.objects.order_by('id')
    context_object_name = 'labels'


class CreateLabelView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'label/base_create_label.html'
    success_url = reverse_lazy('labels')
    form_class = CreateLabelForm
    success_message = _('Метка успешно создана')


class UpdateLabelView(OperationUpdate):
    template_name = 'label/base_update_label.html'
    model = Label
    form_class = CreateLabelForm
    success_message = _('Метка успешно изменена')
    success_url = reverse_lazy('labels')
    redirect_field_name = reverse_lazy('labels')


class DeleteLabelView(OperationDelete):
    template_name = 'label/base_delete_label.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Метка успешно удалена')
    msg_error = _('Невозможно удалить метку, потому что она используется')

    def form_valid(self, form):
        if self.get_object().task.all():
            messages.error(self.request, self.msg_error)
        else:
            super(DeleteLabelView, self).form_valid(form)
        return redirect(self.success_url)
