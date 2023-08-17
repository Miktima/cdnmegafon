from django import forms
from stat_cdnnow.models import Portals_stat

class ClearCacheForm(forms.Form):
    choices_list = [('all', 'All projects')]
    for p in Portals_stat.objects.filter(old_project=False).order_by('portal'):
        choices_list.append((p.pk, p.portal))
    choices = tuple(choices_list)
    project = forms.ChoiceField(label='Select project', choices=choices)
    masks = forms.CharField(label='Masks', max_length=200, required=False)
