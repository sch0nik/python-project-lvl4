# TODO: текст флэш сообщения как в демонстрационном проекте
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from fourth.task_manager.forms import (
    CreateUserForm,
    CreateStatusForm,
    CreateTaskForm,
)
from fourth.task_manager.models import StatusTask, Task


class IndexView(TemplateView):
    template_name = 'base_index.html'


class UsersView(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'users/base_list_user.html'
    context_object_name = 'users'


class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'users/base_create_user.html'
    success_url = reverse_lazy('login')
    form_class = CreateUserForm
    success_message = _('Пользователь создан')


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'users/base_login_user.html'
    next_page = reverse_lazy('index')
    success_message = _('Вы залогинены')
    success_url = reverse_lazy('index')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class UpdateUserView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = User
    login_url = reverse_lazy('login')
    template_name = 'users/base_update_user.html'
    form_class = CreateUserForm
    success_message = _('Пользователь изменен')
    redirect_field_name = reverse_lazy('login')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('У вас нет прав для изменения другого пользователя')
        )
        return redirect('users')


class DeleteUserView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView
):
    template_name = 'users/base_delete_user.html'
    model = User
    success_url = reverse_lazy('users')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    success_message = _('Пользователь удален')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('У вас нет прав для изменения другого пользователя'),
        )
        return redirect('users')

    def form_valid(self, form):
        if self.request.user.executor:
            messages.error(
                self.request,
                _('Невозможно удалить пользователя, потому что он используется'),
            )
        return redirect('users')


class StatusesView(LoginRequiredMixin, ListView):
    template_name = 'status/base_list_statuses.html'
    queryset = StatusTask.objects.order_by('id')
    context_object_name = 'statuses'

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status/base_create_status.html'
    success_url = reverse_lazy('statuses')
    form_class = CreateStatusForm
    success_message = _('Статус создан')


class UpdateStatusView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
):
    template_name = 'status/base_update_status.html'
    model = StatusTask
    login_url = reverse_lazy('login')
    form_class = CreateStatusForm
    success_message = _('Статус изменен')
    success_url = reverse_lazy('statuses')
    redirect_field_name = reverse_lazy('statuses')

    def test_func(self):
        return self.request.__dict__['resolver_match'].kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class DeleteStatusView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView
):
    template_name = 'status/base_delete_status.html'
    model = StatusTask
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    success_message = _('Статус удален')

    def get_context_data(self, **kwargs):
        context = super(DeleteStatusView, self).get_context_data()
        ind = self.request.__dict__['resolver_match'].kwargs['pk']
        context['status'] = StatusTask.objects.get(id=ind)
        return context

    def test_func(self):
        return self.request.__dict__['resolver_match'].kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'task/base_list_task.html'
    queryset = Task.objects.order_by('id')
    context_object_name = 'tasks_list'

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'task/base_create_task.html'
    success_url = reverse_lazy('tasks')
    form_class = CreateTaskForm
    success_message = _('Задача создана')

    def form_valid(self, form):
        new = form.save(commit=False)
        new.autor = self.request.user
        new.save()
        return super().form_valid(form)


class UpdateTaskView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
):
    template_name = 'task/base_update_task.html'
    model = Task
    login_url = reverse_lazy('login')
    form_class = CreateTaskForm
    success_message = _('Задача изменена')
    success_url = reverse_lazy('tasks')
    redirect_field_name = reverse_lazy('tasks')

    def test_func(self):
        return self.request.__dict__['resolver_match'].kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class DeleteTaskView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView
):
    template_name = 'task/base_delete_task.html'
    model = Task
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    redirect_field_name = None
    success_message = _('Задача удалена')

    def get_context_data(self, **kwargs):
        context = super(DeleteTaskView, self).get_context_data()
        ind = self.request.__dict__['resolver_match'].kwargs['pk']
        context['task'] = Task.objects.get(id=ind)
        return context

    def test_func(self):
        return self.request.__dict__['resolver_match'].kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')

    def get(self, request, *args, **kwargs):
        pk = self.request.__dict__['resolver_match'].kwargs['pk']
        autor = Task.objects.get(id=pk).autor
        if autor == self.request.user:
            return super(DeleteTaskView, self).post(self, request, *args, **kwargs)
        else:
            messages.error(self.request, _('Задачу может удалить только её автор'))
            return redirect('tasks')


class TaskView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = 'task/base_detail_task.html'
    model = Task
