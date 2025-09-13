# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from gestione_hotel.models import Hotel # Importiamo il modello Hotel dall'altra app

class UserProfile(models.Model):
    # Il collegamento 1-a-1 al modello Utente di Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    
    # La lista di hotel a cui questo utente può accedere
    allowed_hotels = models.ManyToManyField(
        Hotel, 
        # 'blank=True' significa che un utente può anche non essere associato a nessun hotel
        blank=True,
        verbose_name="Hotel Abilitati"
    )

    def __str__(self):
        return self.user.username