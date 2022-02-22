from django.shortcuts import render
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/index.html', context={'var': ''})
