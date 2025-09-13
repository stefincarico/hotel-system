# booking/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Prenotazione, Stanza

class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['cliente', 'stanza', 'data_check_in', 'data_check_out']
        # Escludiamo 'hotel' e 'stato', li imposteremo automaticamente nella view.
        widgets = {
            'data_check_in': forms.DateInput(attrs={'type': 'date'}),
            'data_check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Prendiamo l'hotel passato dalla view
        hotel = kwargs.pop('hotel', None)
        super().__init__(*args, **kwargs)
        if hotel:
            # Filtriamo il queryset delle stanze per mostrare solo quelle dell'hotel corrente
            self.fields['stanza'].queryset = Stanza.objects.filter(hotel=hotel)

    def clean(self):
        cleaned_data = super().clean()
        stanza = cleaned_data.get("stanza")
        data_check_in = cleaned_data.get("data_check_in")
        data_check_out = cleaned_data.get("data_check_out")

        if stanza and data_check_in and data_check_out:
            # Controlliamo che la data di check-out sia dopo quella di check-in
            if data_check_out <= data_check_in:
                raise ValidationError(
                    "La data di check-out deve essere successiva alla data di check-in."
                )

            # Controlliamo le sovrapposizioni
            prenotazioni_in_conflitto = Prenotazione.objects.filter(
                stanza=stanza,
                data_check_out__gt=data_check_in,
                data_check_in__lt=data_check_out
            ).exclude(pk=self.instance.pk) # Escludiamo noi stessi se siamo in modalità modifica

            if prenotazioni_in_conflitto.exists():
                raise ValidationError(
                    "Questa stanza è già occupata nelle date selezionate."
                )

        return cleaned_data