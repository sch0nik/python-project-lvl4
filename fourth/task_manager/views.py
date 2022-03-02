import os
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from django.views.generic import ListView


# class User():
#     pass


class IndexView(TemplateView):
    template_name = 'base.html'


class UsersView(ListView):
    queryset = User.objects.order_by('id')
    template_name = 'base_users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context['active'] = 'active'
        return context


class RegisterView(CreateView):
    template_name = 'base_register.html'
    model = User
    fields = ['username', 'first_name', 'last_name', 'password']
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['active'] = 'active'
        context['msg'] = 'Такой пользователь уже есть'
        return context


class LoginView(TemplateView):
    template_name = 'base_login.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context={
                'active': 'active'
            }
        )

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            msg = "Неверные логин или пароль"
            return render(request, self.template_name, context={
                'msg': msg,
                'active': 'active'
            })


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class UpdateView(TemplateView):
    template_name = 'update.html'


class DeleteView(TemplateView):
    template_name = 'base_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={
            'user': User.objects.get(),
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            msg = "Неверные логин или пароль"
            return render(request, self.template_name, context={
                'msg': msg,
                'active': 'active'
            })
