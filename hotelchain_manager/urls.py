"""
URL configuration for hotelchain_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from gestione_hotel.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 👇 LA NOSTRA NUOVA, POTENTE RIGA!
    # "Tutte le rotte che iniziano con 'hotel/' devono essere gestite
    # dal file urls.py che si trova nell'app 'gestione_hotel'".
    path('hotel/', include('gestione_hotel.urls', namespace='hotel')),
    
    # Per ora, potremmo voler mantenere una homepage "radice" del sito.
    # Possiamo importare la view e creare una rotta apposita se vogliamo,
    # oppure decidere che la lista hotel è la nostra homepage.
    # Per semplicità, diciamo che la lista hotel è la nostra homepage
    # per ora, e la deleghiamo sempre alla nostra app.
    path('', include('gestione_hotel.urls')), # Potremmo fare così per la radice
    
    # Sovrascriviamo solo l'URL di logout per accettare GET
    path('accounts/logout/', logout_view, name='logout'),
    # Usiamo le view di default per il login, reset password etc
    path('accounts/', include('django.contrib.auth.urls')),
]