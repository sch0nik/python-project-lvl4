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

from fourth.task_manager.forms import CreateUserForm


class IndexView(TemplateView):
    template_name = 'base_index.html'


class UsersView(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'base_users.html'
    context_object_name = 'users'


class CreateUserView(CreateView):
    template_name = 'base_create.html'
    success_url = reverse_lazy('login')
    form_class = CreateUserForm


class LoginUserView(LoginView):
    template_name = 'base_login.html'
    next_page = reverse_lazy('index')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class UpdateUserView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = User
    success_url = reverse_lazy('login')
    template_name = 'base_update.html'
    form_class = CreateUserForm
    success_message = _('Пользователь изменен')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return redirect('users')


class DeleteUserView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'base_delete.html'
    model = User
    success_url = reverse_lazy('users')
    login_url = reverse_lazy('login')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        return redirect('users')
