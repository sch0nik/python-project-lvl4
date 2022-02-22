from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/index.html', context={'var': ''})
