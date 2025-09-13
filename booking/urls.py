# booking/urls.py
from django.urls import path
from .views import prenotazione_create_view, prenotazione_update_view, prenotazione_cancel_view

app_name = 'booking'

urlpatterns = [
    path('hotel/<int:hotel_pk>/nuova/', prenotazione_create_view, name='prenotazione_create'),
    # 👇 LE NOSTRE NUOVE ROTTE!
    path('prenotazione/<int:pk>/modifica/', prenotazione_update_view, name='prenotazione_update'),
    path('prenotazione/<int:pk>/annulla/', prenotazione_cancel_view, name='prenotazione_cancel'),
]