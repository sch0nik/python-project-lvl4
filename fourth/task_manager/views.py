# TODO: флэш сообщения как в демонстрационном проекте
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from fourth.task_manager.forms import CreateUserForm, CreateStatusForm
from fourth.task_manager.models import StatusTask


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
    SuccessMessageMixin,
    LoginRequiredMixin,
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
    SuccessMessageMixin,
    LoginRequiredMixin,
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


class StatusesView(LoginRequiredMixin, ListView):
    template_name = 'status/base_list_statuses.html'
    queryset = StatusTask.objects.order_by('id')
    context_object_name = 'statuses'

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class CreateStatusView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'status/base_create_status.html'
    success_url = reverse_lazy('statuses')
    form_class = CreateStatusForm
    success_message = _('Статус создан')


class UpdateStatusView(
    SuccessMessageMixin,
    LoginRequiredMixin,
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
    SuccessMessageMixin,
    LoginRequiredMixin,
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


class TaskListView:
    pass


class CreateTaskView:
    pass


class UpdateTaskView:
    pass


class DeleteTaskView:
    pass


class TaskView:
    pass
