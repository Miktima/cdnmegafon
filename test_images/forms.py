from django import forms

class CdnForm(forms.Form):
    page_url = forms.URLField(label='Page URL', max_length=200)
    old_cdn = forms.CharField(label='CDN on the page', max_length=200)
    new_cdn = forms.CharField(label='New CDN', max_length=200, required=False)