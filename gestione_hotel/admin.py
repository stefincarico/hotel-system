# gestione_hotel/admin.py

from django.contrib import admin
from .models import Stanza, Hotel

class StanzaAdmin(admin.ModelAdmin):
    list_display = ('numero','hotel', 'tipologia',  'ospiti_massimo', 'ha_problemi',)
    list_filter = ('hotel', 'tipologia','ha_problemi')
    search_fields = ('numero', 'hotel__nome', 'descrizione')
    list_editable = ( 'ha_problemi',)  # Permette di modificare direttamente dalla lista
    list_per_page = 10  # Numero di elementi per pagina

# Registra il modello con la classe Admin personalizzata
admin.site.register(Stanza, StanzaAdmin)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'indirizzo', 'stato')  # Aggiungi i campi che vuoi visualizzare
    list_filter = ('stato',)  # Aggiungi filtri laterali
    search_fields = ('nome', 'indirizzo')  # Aggiungi campi di ricerca

# Registra il modello con la classe Admin personalizzata
admin.site.register(Hotel, HotelAdmin)