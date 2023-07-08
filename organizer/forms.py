from django import forms
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import organizerRecord

ID_TYPE = [('VOTER_ID', 'VOTER_ID'), ('LICENSE', 'LICENSE'), ('PASSPORT', 'PASSPORT'), ('ADHAAR', 'ADHAAR'), ('PAN_CARD', 'PAN_CARD')]


class organizerForm(forms.ModelForm): 
    Fname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first name'}), required=True, max_length=30)
    Lname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=True, max_length=30)
    Mobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile No'}),
        required=True, max_length=10)
    Email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True)
    Dob = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    Profile_pic = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)
    Address = description = forms.CharField(widget=CKEditorUploadingWidget())
    Id_type = forms.EmailField(
        label='ID TYPE', widget=forms.Select(choices=ID_TYPE, attrs={'class': 'form-control'}), required=True)
    Id_file = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)

    class Meta:
        model = organizerRecord
        fields = ['Fname', 'Lname', 'Mobile', 'Email', 'Dob', 'Profile_pic','Address','Id_type','Id_file']

    def clean_email(self):
        Email = None
        try:
            Email = self.cleaned_data['Email']
            organizerRecord.objects.get(Email=Email)
            raise forms.ValidationError("Email already taken. Try to login")
        except ObjectDoesNotExist:
            return Email