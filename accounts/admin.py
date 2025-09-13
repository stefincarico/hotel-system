# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Definiamo un "inline" per il nostro profilo,
# in modo da poterlo modificare direttamente dalla pagina dell'utente
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profili'

# Estendiamo l'Admin base dell'Utente
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# De-registriamo il UserAdmin di base e registriamo il nostro personalizzato
admin.site.unregister(User)
admin.site.register(User, UserAdmin)