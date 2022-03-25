from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from apps.status_app.forms import CreateStatusForm
from apps.status_app.models import StatusTask
from task_manager.mixins import OperationList, OperationUpdate, OperationDelete


class StatusesView(OperationList):
    template_name = 'status/base_list_status.html'
    queryset = StatusTask.objects.order_by('id')
    context_object_name = 'statuses'


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status/base_create_status.html'
    success_url = reverse_lazy('statuses')
    form_class = CreateStatusForm
    success_message = _('Статус успешно создан')


class UpdateStatusView(OperationUpdate):
    model = StatusTask
    template_name = 'status/base_update_status.html'
    form_class = CreateStatusForm
    success_message = _('Статус успешно изменён')
    success_url = reverse_lazy('statuses')
    redirect_field_name = reverse_lazy('statuses')


class DeleteStatusView(OperationDelete):
    model = StatusTask
    template_name = 'status/base_delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Статус успешно удалён')
    msg_error = _('Невозможно удалить статус, потому что он используется')

    def form_valid(self, form):
        if self.get_object().task.all():
            messages.error(self.request, self.msg_error)
        else:
            super(DeleteStatusView, self).form_valid(form)
        return redirect(self.success_url)
