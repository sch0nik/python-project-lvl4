import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView

import fourth.settings


class IndexView(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={
            'msg': list({
                'DEBUG': fourth.settings.DEBUG,
                'STATIC': fourth.settings.STATIC_URL,
                'PATH': os.getcwd(),
                'BASE_DIR': fourth.settings.BASE_DIR,
            }.items()),
        })


class UsersView(TemplateView):
    template_name = 'base_users.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context={
                'users': User.objects.order_by('id'),
                'active': 'active'
            },
        )


class RegisterView(TemplateView):
    template_name = 'base_register.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context={
                'active': 'active'
            }
        )

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.filter(username=username)
        if user:
            return render(
                request,
                self.template_name,
                context={
                    'msg': 'Такой пользователь уже есть',
                    'active': 'active'
                }
            )
        if password1 == password2:
            user = User()
            user.username = username
            user.set_password(password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(
                request,
                self.template_name,
                context={
                    'msg': 'Такой пользователь уже есть',
                    'active': 'active'
                },
            )


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
            msg = "Логин или пароль неверные"
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
    template_name = 'delete.html'
