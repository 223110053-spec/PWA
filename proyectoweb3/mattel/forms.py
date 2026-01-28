from django import forms
from .models import Contacto
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre','email','telefono','mensaje']
        widgets = {'mensaje': forms.Textarea(attrs={'rows':4})}
