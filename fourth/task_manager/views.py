from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'main': 'main.html'})


class UsersView(TemplateView):
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'users.html',
            context={'users': User.objects.all()},
        )


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
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
                context={'msg': 'Такой пользователь уже есть'}
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
                context={'msg': 'Пароли не сопадают'},
            )


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
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
            return render(request, self.template_name, context={'msg': msg})


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class UpdateView(TemplateView):
    template_name = 'update.html'


class DeleteView(TemplateView):
    template_name = 'delete.html'
