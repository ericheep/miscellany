from django import forms
from .models import Work, Performance, Venue


class WorkForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 70, 'rows': 15})
    )

    created_date = forms.DateField(
        label='Date',
        widget=forms.TextInput(attrs={'placeholder': 'YY-MM-DD'})
    )

    field_order = ['title', 'text', 'created_date']

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
        empty_label="(nil)"
    )

    event = forms.CharField(
        max_length=100,
    )

    date = forms.DateField(
        widget=forms.TextInput(attrs={'placeholder': 'YY-MM-DD'})
    )

    field_order = ['work', 'venue', 'event', 'date']

    class Meta:
        model = Performance
        fields = {}


class VenueForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
    )

    address = forms.CharField(
        max_length=200,
    )

    field_order = ['name', 'address']

    class Meta:
        model = Performance
        fields = {}
