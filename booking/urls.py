# booking/urls.py
from django.urls import path
from .views import prenotazione_create_view

app_name = 'booking'

urlpatterns = [
    # La nostra view di creazione sarà relativa a un hotel specifico
    path('hotel/<int:hotel_pk>/nuova/', prenotazione_create_view, name='prenotazione_create'),
]