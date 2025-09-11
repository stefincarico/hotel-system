# gestione_hotel/admin.py

from django.contrib import admin
from .models import Stanza, Hotel

# Register your models here.

admin.site.register(Stanza)  # 👈 2. Registriamo Stanza nel sito di amministrazione
admin.site.register(Hotel) # 👈 2. Registriamo Hotel