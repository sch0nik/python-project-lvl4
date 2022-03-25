from django import forms

from apps.status_app.models import StatusTask


class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = StatusTask
        fields = ('name',)
