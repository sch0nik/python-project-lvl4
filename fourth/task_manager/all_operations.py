from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DeleteView, UpdateView

from fourth.task_manager.models import Label


class OperationList(LoginRequiredMixin, ListView):

    def handle_no_permission(self):
        messages.error(self.request, _('Вы не авторизованы'))
        return redirect('login')


class OperationDelete(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView
):
    login_url = reverse_lazy('login')
    redirect_field_name = None
    condition = None
    msg_error = ''
    msg_login_error = _('Вы не авторизованы')

    def get_context_data(self, **kwargs):
        context = super(OperationDelete, self).get_context_data()
        context['object_del'] = self.get_object()
        return context

    def test_func(self):
        return self.kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, self.msg_login_error)
        return redirect('login')


class OperationUpdate(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
):
    login_url = reverse_lazy('login')
    msg_login_error = _('Вы не авторизованы')

    def test_func(self):
        return self.kwargs['pk'] == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, self.msg_login_error)
        return redirect('login')
