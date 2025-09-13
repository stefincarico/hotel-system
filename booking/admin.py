# booking/admin.py

from django.contrib import admin
from .models import Cliente, Prenotazione

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'email', 'telefono')
    search_fields = ('nome', 'cognome', 'email')

@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'hotel', 'stanza', 'data_check_in', 'data_check_out', 'stato')
    list_filter = ('stato', 'hotel', 'data_check_in')
    search_fields = ('cliente__nome', 'cliente__cognome', 'stanza__numero')
    autocomplete_fields = ['cliente', 'hotel', 'stanza'] # Rende la selezione più facile!