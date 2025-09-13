from django.db import models
from gestione_hotel.models import Hotel, Stanza

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return f"{self.nome} {self.cognome}"
    

# Modello che rappresenta la prenotazione
class Prenotazione(models.Model):
    # Definiamo uno stato per la prenotazione
    class StatoPrenotazione(models.TextChoices):
        CONFERMATA = 'CONFERMATA', 'Confermata'
        CANCELLATA = 'CANCELLATA', 'Cancellata'
        COMPLETATA = 'COMPLETATA', 'Completata' # Dopo il check-out

    # --- RELAZIONI CHIAVE (ForeignKey) ---
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="prenotazioni")
    stanza = models.ForeignKey(Stanza, on_delete=models.CASCADE, related_name="prenotazioni")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="prenotazioni")

    # --- DATE DELLA PRENOTAZIONE ---
    data_check_in = models.DateField()
    data_check_out = models.DateField()

    # --- ALTRI DETTAGLI ---
    stato = models.CharField(
        max_length=10,
        choices=StatoPrenotazione.choices,
        default=StatoPrenotazione.CONFERMATA
    )
    creata_il = models.DateTimeField(auto_now_add=True) # Data e ora di creazione, impostata automaticamente
    modificata_il = models.DateTimeField(auto_now=True) # Data e ora ultima modifica, aggiornata automaticamente

    class Meta:
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"
        # Ordiniamo le prenotazioni per data di check-in di default
        ordering = ['-data_check_in']

    def __str__(self):
        return f"Prenotazione per {self.cliente} - Stanza {self.stanza.numero} ({self.hotel.nome})"
