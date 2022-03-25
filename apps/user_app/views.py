from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from apps.user_app.forms import CreateUserForm
from apps.user_app.models import User
from task_manager.mixins import OperationUpdate, OperationDelete


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
