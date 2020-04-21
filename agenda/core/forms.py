from django import forms

from .models import Agenda


class AgendaForm(forms.ModelForm):
    horarios = forms.MultipleChoiceField()

    class Meta:
        model = Agenda
        fields = ['medico', 'dia']
