from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'main': 'main.html'})


class UsersView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        users = loader.render_to_string('users.html', context={})
        return render(request, 'index.html', context={'main': users})
