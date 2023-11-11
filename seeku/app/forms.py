from django import forms
from .models import Object,Claim_Complaint

class BlockFilterForm(forms.Form):
    block_checkboxes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
class ClaimObject(forms.ModelForm):
    user_comment = forms.CharField(
    label='Añade una descripción de tu objeto',
    widget=forms.Textarea(attrs={'placeholder': 'Entre más específica la descripción, mejor'}))
    class Meta:
        model=Object
        fields=['place_found','date_found','brands','color']
        labels={'place_found':'Dinos dónde perdiste tu objecto',
                'date_found':'Dinos qué día perdiste tu objeto',
                'brands':'Qué marca es tu objeto',
                'color':'De qué color es tu objeto',
        }
        widgets = {
            'date_found': forms.DateInput(attrs={'type': 'date'}),
        }
        
class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ['title', 'description', 'brands', 'image', 'date_found', 'place_found', 'hour_range', 'color', 'category','place_registered', 'object_status', 'object_recovered']  # Add all fields here

class DeleteForm(forms.Form):
  id = forms.IntegerField(required=True)
  
class ClaimComplaint(forms.ModelForm):
    class Meta:
        model=Claim_Complaint
        exclude=['user_email','object_related','date_lost']
        labels={'time_initial':'Time you knew you had the object',
                'time_final':'Time you realized you lost the object'
        }
        widgets={
            'time_initial': forms.TimeInput(attrs={'format':"%H:%M",'type':'time','input_type':'time_24h'}),
            'time_final': forms.TimeInput(attrs={'format':"%H:%M",'type':'time','input_type':'time_24h'}),
            'extra_data':forms.Textarea(attrs={'placeholder':'Plase specify us the place, like the floor, did you lose it in a bathroom, etc.'})
          #'date_lost': forms.DateInput(attrs={'type': 'date'})
        }