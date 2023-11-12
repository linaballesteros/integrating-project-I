from django import forms
from .models import Object

class BlockFilterForm(forms.Form):
    block_checkboxes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
class ClaimObject_es(forms.ModelForm):
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
class ClaimObject(forms.ModelForm):
    class Meta:
        model=Object
        fields=['place_found','date_found','brands','color']
        labels={'place_found':'Where did you lose your object?',
                'date_found':'Which day did you lose your object?',
                'brands':'What is the brand of your object?',
                'color':'What is the color of your object?'}
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'})
        }
        
class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['title', 'description', 'brands', 'image', 'date_found', 'place_found', 'hour_range', 'color', 'category','place_registered', 'object_status', 'object_recovered', 'complaints_amount'] 

class DeleteForm(forms.Form):
  id = forms.IntegerField(required=True)
