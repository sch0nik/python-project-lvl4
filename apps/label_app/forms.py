from django import forms

from apps.label_app.models import Label


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name',)


