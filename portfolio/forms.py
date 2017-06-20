from django import forms
from .models import Work, Performance


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = {'title', 'text'}


class PerformanceForm(forms.ModelForm):

    class Meta:
        model = Performance
        fields = {'work', 'venue', 'event', 'date'}
