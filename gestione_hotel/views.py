# gestione_hotel/views.py

from django.shortcuts import get_object_or_404, render,redirect
from .models import Hotel, Stanza
from .forms import HotelForm # 👈 1. Importiamo il modello Hotel

# Create your views here.

def homepage_view(request):
    # 2. Questa è la nostra logica: prendiamo TUTTI gli hotel
    #    ma li filtriamo per avere solo quelli ATTIVI!
    #    L'ordinamento per nome è un tocco di classe.
    lista_hotel_attivi = Hotel.objects.filter(stato=Hotel.StatoHotel.ATTIVO).order_by('nome')

    # 3. Prepariamo il "contesto", cioè i dati da inviare al template.
    #    È un dizionario: la chiave 'hotels' sarà il nome che useremo nel template.
    context = {
        'hotels': lista_hotel_attivi,
    }

    # 4. Diciamo a Django di "renderizzare" (costruire) la risposta.
    #    Gli passiamo la richiesta, il nome del template che vogliamo usare,
    #    e i dati (il contesto).
    return render(request, 'gestione_hotel/homepage.html', context)


# 👇 LA NOSTRA NUOVA VIEW!
def hotel_detail_view(request, pk):
    # 1. Recuperiamo l'hotel specifico usando il pk dall'URL.
    #    Se non esiste, Django mostrerà una pagina 404.
    hotel = get_object_or_404(Hotel, pk=pk)

    # 2. Recuperiamo TUTTE le stanze collegate a QUESTO hotel.
    #    Ricordi il related_name='stanze' nel modello Stanza? Eccolo in azione!
    stanze_dell_hotel = hotel.stanze.all()

    # 3. Prepariamo il contesto per il template.
    context = {
        'hotel': hotel,
        'stanze': stanze_dell_hotel,
    }

    # 4. Renderizziamo il nuovo template di dettaglio
    return render(request, 'gestione_hotel/hotel_detail.html', context)

def hotel_create_view(request):
    # 2. Logica per gestire il POST (invio dati)
    if request.method == 'POST':
        # Creiamo un'istanza del form riempiendola con i dati dal POST
        form = HotelForm(request.POST)
        # Controlliamo se i dati sono validi
        if form.is_valid():
            form.save() # Se è valido, salviamo l'oggetto nel database!
            return redirect('homepage') # Reindirizziamo l'utente alla homepage
    
    # 3. Logica per gestire il GET (prima visita)
    else:
        # Creiamo un'istanza del form vuota
        form = HotelForm()

    # 4. Mandiamo il form (vuoto o con errori) al template
    context = {
        'form': form,
    }
    return render(request, 'gestione_hotel/hotel_create.html', context)