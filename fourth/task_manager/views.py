from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
# from fourth.task_manager.models import Users


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'main': 'main.html'})


class UsersView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        users = loader.render_to_string('users.html', context={
            'users': User.objects.all(),
            # 'users': None,
        })
        # users = loader.render_to_string('users.html')
        return render(request, 'index.html', context={'main': users})
