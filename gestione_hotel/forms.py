# gestione_hotel/forms.py

from django import forms
from .models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        # Specifichiamo i campi che vogliamo nel nostro form.
        # L'ID viene gestito in automatico, quindi non lo includiamo.
        fields = ['nome', 'indirizzo', 'stato']