# gestione_hotel/urls.py

from django.urls import path
from .views import (
    homepage_view, 
    hotel_detail_view, 
    hotel_create_view,
    hotel_update_view,
    hotel_delete_view 
)

# Questo è importante per il namespacing che vedremo dopo!
app_name = 'gestione_hotel'

urlpatterns = [
    # Nota: la rotta per la homepage ora è '' perché il prefisso '/hotel/'
    # verrà gestito dal file urls.py principale.
    path('', homepage_view, name='hotel_list'), # Rinominiamo 'homepage' in 'hotel_list' per chiarezza
    path('nuovo/', hotel_create_view, name='hotel_create'),
    path('<int:pk>/', hotel_detail_view, name='hotel_detail'),
    path('<int:pk>/modifica/', hotel_update_view, name='hotel_update'),
    path('<int:pk>/elimina/', hotel_delete_view, name='hotel_delete'),
]