from django import forms

class LogForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'text/csv, application/zip'}))