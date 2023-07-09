from datetime import date

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import EventRecord

EVENTS = [('workshop', 'Workshop'), ('seminar', 'Seminar')]
MODE = [('public', 'Public'),('private', 'Private') ]

PLATFORM = [('offline', 'offline'),("online", "online")]


class EventForm(forms.ModelForm):

    
    event_title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Event Title'}), required=True, max_length=100)
    
    event_subtitle = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Event Subtitle'}), required=True, max_length=100)
    
    types = forms.CharField(widget=forms.Select(
        choices=EVENTS, attrs={'class': 'form-control'}), required=True)
    
    fees = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Fees'}), min_value=0, max_value=10000, required=True)
    
    description = forms.CharField(widget=CKEditorUploadingWidget())
    
    event_start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    
    event_end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    
    event_start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'form-control'}))
    
    event_end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'type': 'time', 'class': 'form-control'}))
    
    platform = forms.CharField(widget=forms.Select(
        choices=PLATFORM, attrs={'class': 'form-control'}), required=True)
    
    venue = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Venue'}), required=True, max_length=50)
    
    
    mode = forms.CharField(widget=forms.Select(
        choices=MODE, attrs={'class': 'form-control'}), required=True)
    
    registration_start = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    
    registration_end = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    
    no_of_tickets = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'no of tickets'}), min_value=0, max_value=10000, required=True)
    
    category = forms.CharField(widget=forms.Select(
        choices=EVENTS, attrs={'class': 'form-control'}), required=True)
    
    subcategory = forms.CharField(widget=forms.Select(
        choices=EVENTS, attrs={'class': 'form-control'}), required=True)
    
    website = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'website link'}), required=False, max_length=100)
    
    facebook = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'facebook link'}), required=False, max_length=100)
    
    instagram = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'instagram link'}), required=False, max_length=100)
    
    youtube = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'youtube link'}), required=False, max_length=100)
    
    banner = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)
    
    poster = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)
    
    logo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)
    
    sponsor_logo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)
    
    

    class Meta:
        model = EventRecord
        fields = ['event_title', 'event_subtitle', 'fees', 'description', 'event_start_date', 'event_end_date',
                  'event_start_time', 'event_end_time', 'venue', 'mode', 'registration_start', 'registration_end', 'no_of_tickets',
                  'category', 'subcategory', 'website', 'facebook', 'instagram',
                  'youtube', 'banner', 'poster', 'logo','platform','types',
                  'sponsor_logo']

    def clean_registration_start(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            if True or registration_start.strftime('%Y-%m-%d') >= date.today().strftime('%Y-%m-%d'):
                return registration_start
            # raise forms.ValidationError("Invalid Start Date")
        except Exception:
            raise forms.ValidationError("Invalid Start Date")

    def clean_registration_end(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            registration_end = self.cleaned_data['registration_end']
            if registration_start <= registration_end:
                return registration_end
            raise forms.ValidationError("Invalid End Date")
        except Exception:
            raise forms.ValidationError("Invalid End Date")

    def clean_event_date(self):
        try:
            registration_start = self.cleaned_data['registration_start']
            event_date = self.cleaned_data['event_date']
            if registration_start <= event_date:
                return event_date
            raise forms.ValidationError("Invalid Event Date")
        except Exception:
            raise forms.ValidationError("Invalid Event Date")
