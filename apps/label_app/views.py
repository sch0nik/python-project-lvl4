from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from apps.label_app.forms import CreateLabelForm
from apps.label_app.models import Label
from task_manager.mixins import OperationList, OperationUpdate, OperationDelete


class LabelsView(OperationList):
    template_name = 'label/base_list_label.html'
    queryset = Label.objects.order_by('id')
    context_object_name = 'labels'


class CreateLabelView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'label/base_create_label.html'
    success_url = reverse_lazy('labels')
    form_class = CreateLabelForm
    success_message = _('Метка успешно создана')


class UpdateLabelView(OperationUpdate):
    template_name = 'label/base_update_label.html'
    model = Label
    form_class = CreateLabelForm
    success_message = _('Метка успешно изменена')
    success_url = reverse_lazy('labels')
    redirect_field_name = reverse_lazy('labels')


class DeleteLabelView(OperationDelete):
    template_name = 'label/base_delete_label.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Метка успешно удалена')
    msg_error = _('Невозможно удалить метку, потому что она используется')

    def form_valid(self, form):
        if self.get_object().task.all():
            messages.error(self.request, self.msg_error)
        else:
            super(DeleteLabelView, self).form_valid(form)
        return redirect(self.success_url)
