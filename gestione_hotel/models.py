# gestione_hotel/models.py

from django.db import models

# Create your models here.

class Stanza(models.Model):
    # Il numero della stanza, es: 101, 202...
    numero = models.IntegerField()

    # La tipologia, es: "Singola", "Matrimoniale", "Suite"
    # max_length è obbligatorio per i CharField
    tipologia = models.CharField(max_length=50)

    # Quanti ospiti può accogliere al massimo
    ospiti_massimo = models.IntegerField()

    # Un semplice flag per la manutenzione
    ha_problemi = models.BooleanField(default=False)

        # 👇 IL NOSTRO NUOVO CAMPO!
    # Un campo di testo per descrivere il problema.
    # "blank=True" significa che il campo non è obbligatorio (può essere vuoto).
    # "null=True" dice al database che può accettare un valore nullo.
    # Perfetto per noi: questo campo avrà valore solo se ha_problemi è True!
    descrizione_problema = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Stanza N° {self.numero} - {self.tipologia}"