from django import forms
from .models import Object
class ClaimObject(forms.ModelForm):
    class Meta:
        model=Object
        fields=['place_found','date_found','brands','color']
        labels={'place_found':'Dinos dónde perdiste tu objecto',
                'date_found':'Dinos qué día perdiste tu objeto',
                'brands':'Qué marca es tu objeto',
                'color':'De qué color es tu objeto'}
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'})
        }