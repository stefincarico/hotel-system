# booking/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Prenotazione, Stanza

# 👇 IMPORTIAMO GLI OGGETTI PER IL LAYOUT
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.layout import Submit

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

        # Correzione: impostiamo manualmente il valore iniziale per i campi data.
        # Questo forza il valore nel widget nel caso in cui il meccanismo di default fallisca.
        if self.instance and self.instance.pk:
            if self.instance.data_check_in:
                self.initial['data_check_in'] = self.instance.data_check_in.strftime('%Y-%m-%d')
            if self.instance.data_check_out:
                self.initial['data_check_out'] = self.instance.data_check_out.strftime('%Y-%m-%d')
        
        # 1. Creiamo un'istanza dell'helper
        self.helper = FormHelper()
        
        # 2. Definiamo il layout del nostro form
        self.helper.layout = Layout(
            # Mettiamo i campi 'cliente' e 'stanza' uno dopo l'altro
            'cliente',
            'stanza',
            
            # Ora creiamo una riga per le date
            Row(
                # La prima colonna conterrà il campo 'data_check_in'
                # 'col-md-6' è una classe di Bootstrap che dice "su schermi medi e grandi, occupa 6/12 (metà) dello spazio"
                Column('data_check_in', css_class='form-group col-md-6 mb-0'),
                
                # La seconda colonna conterrà 'data_check_out'
                Column('data_check_out', css_class='form-group col-md-6 mb-0'),
                
                # 'css_class' sulla Row si applica alla riga stessa
                css_class='form-row'
            ),
            
            # Se avessimo altri campi, potremmo continuare a metterli qui
        )
        # Il testo del bottone cambia se stiamo modificando o creando
        if self.instance and self.instance.pk:
            self.helper.add_input(Submit('submit', 'Salva Modifiche', css_class='btn-primary mt-3'))
        else:
            self.helper.add_input(Submit('submit', 'Crea Prenotazione', css_class='btn-primary mt-3'))


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