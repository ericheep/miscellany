from django import forms
from .models import Work, Performance, Venue


class WorkForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
    )

    text = forms.CharField(
        widget=forms.Textarea
    )

    field_order = ['title', 'text']

    class Meta:
        model = Work
        fields = {}


class PerformanceForm(forms.ModelForm):
    work = forms.ModelChoiceField(
        queryset=Work.objects,
        empty_label="(nil)"
    )

    venue = forms.ModelChoiceField(
        queryset=Venue.objects,
        empty_label="(nil)")

    event = forms.CharField(
        max_length=100
    )

    date = forms.DateField(
        help_text="YY-MM-DD",
    )

    field_order = ['work', 'venue', 'event', 'date']

    class Meta:
        model = Performance
        fields = {}
        # help_texts = {
        #     'date': "YY-MM-DD",
        # }
