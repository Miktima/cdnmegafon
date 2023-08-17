from django import forms

class CashForm(forms.Form):
    page_url = forms.URLField(label='Page URL', max_length=255)
    cdn = forms.CharField(label='CDN on the page', max_length=200)
