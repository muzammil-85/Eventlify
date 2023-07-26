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
    Email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True) 
    Mobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mobile No'}),
        required=True, max_length=10)
    Dob = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    
    Address = forms.CharField(widget=CKEditorUploadingWidget())
    Id_type = forms.CharField(
        label='ID TYPE', widget=forms.Select(choices=ID_TYPE, attrs={'class': 'form-control'}), required=True)
    Id_file = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'class': 'custom-file-input', 'style': "opacity:1"}), required=True)

    class Meta:
        model = organizerRecord
        fields = ['Fname', 'Lname', 'Mobile', 'Email', 'Dob','Address','Id_type','Id_file']
    def clean_Email(self):
        email = self.cleaned_data['Email']
        try:
            organizerRecord.objects.get(Email=email)
            raise forms.ValidationError("Email already taken. Try to login")
        except organizerRecord.DoesNotExist:
            return email
