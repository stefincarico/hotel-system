# gestione_hotel/models.py

from django.db import models

class HotelManager(models.Manager):
    def get_queryset_for_user(self, user):
        """
        Restituisce la QuerySet di hotel filtrata per un utente specifico.
        """
        # Se l'utente è un superuser, può vedere tutto.
        if user.is_superuser:
            return super().get_queryset()
        
        # Altrimenti, restituiamo solo gli hotel a cui è abilitato.
        # Usiamo 'user.userprofile' per accedere al profilo.
        # Il .distinct() previene eventuali duplicati se ci fossero relazioni complesse.
        return user.userprofile.allowed_hotels.all().distinct()

# 👇 IL NOSTRO NUOVO MODELLO!
class Hotel(models.Model):
    # 👇 DEFINIAMO GLI STATI POSSIBILI
    class StatoHotel(models.TextChoices):
        ATTIVO = 'ATTIVO', 'Attivo'
        CHIUSO = 'CHIUSO', 'Chiuso'
        ARCHIVIATO = 'ARCHIVIATO', 'Archiviato'

    nome = models.CharField(max_length=100, unique=True) # Aggiungiamo unique=True!
    indirizzo = models.CharField(max_length=255)

    # 👇 AGGIUNGIAMO IL NUOVO CAMPO
    stato = models.CharField(
        max_length=10,
        choices=StatoHotel.choices,
        default=StatoHotel.ATTIVO # Ogni nuovo hotel parte come ATTIVO
    )
    # 👇 COLLEGIAMO IL MANAGER STANDARD E IL NOSTRO NUOVO MANAGER!
    # Django ci dà sempre un manager di base chiamato 'objects'.
    objects = models.Manager() 
    # Ora aggiungiamo il nostro!
    by_user = HotelManager()


    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotel" # Correggiamo anche il plurale in italiano

    def __str__(self):
        return self.nome


class Stanza(models.Model):
    class TipoStanza(models.TextChoices):
        SINGOLA = 'SING', 'Singola'
        MATRIMONIALE = 'MATR', 'Matrimoniale'
        DOPPIA = 'DOPP', 'Doppia con Letti Singoli'
        TRIPLA = "TRIP", 'Tripla'
        SUITE = 'SUIT', 'Suite'

    # 👇 LA NOSTRA NUOVA FOREIGN KEY!
    # Il primo argomento è il modello genitore.
    # on_delete=models.CASCADE è la regola di cancellazione.
    # related_name ci servirà in futuro per le query inverse.
    hotel = models.ForeignKey(Hotel, related_name='stanze', on_delete=models.PROTECT)

    # Il numero della stanza, es: 101, 202...
    numero = models.IntegerField()

    # La tipologia, es: "Singola", "Matrimoniale", "Suite"
    # max_length è obbligatorio per i CharField
    tipologia = models.CharField(
        max_length=4,
        choices=TipoStanza.choices,
        default=TipoStanza.MATRIMONIALE,
    )

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

        # 👇 AGGIUNGIAMO QUESTA PARTE!
    class Meta:
        verbose_name = "Stanza"
        verbose_name_plural = "Stanze"

    def __str__(self):
        return f"Stanza N° {self.numero} ({self.tipologia}) - {self.hotel.nome}"