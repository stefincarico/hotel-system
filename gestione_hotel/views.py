# gestione_hotel/views.py

from django.shortcuts import get_object_or_404, render,redirect
from .models import Hotel, Stanza
from booking.models import Prenotazione
from .forms import HotelForm # 👈 1. Importiamo il modello Hotel
from django.contrib.auth.decorators import login_required # 👈 1. Importiamo il decoratore
from django.contrib.auth import logout
from django.contrib import messages 
from .decorators import custom_login_required
from django.contrib.auth.decorators import permission_required
from django.utils import timezone

# Create your views here.

@login_required
def homepage_view(request):
    # 👇 GUARDA CHE PULIZIA!
    # Chiamiamo il nostro nuovo manager, passandogli l'utente corrente.
    # La logica superuser/utente normale è ora NASCOSTA dentro il manager.
    lista_hotel_attivi = Hotel.by_user.get_queryset_for_user(request.user).filter(
        stato=Hotel.StatoHotel.ATTIVO
    ).order_by('nome')

    context = {
        'hotels': lista_hotel_attivi,
    }
    return render(request, 'gestione_hotel/homepage.html', context)

@login_required
def hotel_detail_view(request, pk):
    # 👇 ANCHE QUI, USIAMO IL NUOVO MANAGER COME PUNTO DI PARTENZA
    # per la nostra QuerySet sicura.
    queryset_sicura = Hotel.by_user.get_queryset_for_user(request.user)
    hotel = get_object_or_404(queryset_sicura, pk=pk)

    # Il resto della view è identico...
    stanze_dell_hotel = hotel.stanze.all()
    prenotazioni_dell_hotel = Prenotazione.objects.filter(stanza__hotel=hotel).order_by('-data_check_in')
    context = {
        'hotel': hotel,
        'stanze': stanze_dell_hotel,
        'prenotazioni': prenotazioni_dell_hotel,
    }
    return render(request, 'gestione_hotel/hotel_detail.html', context)

@permission_required('gestione_hotel.add_hotel', raise_exception=True)
def hotel_create_view(request):
    # 2. Logica per gestire il POST (invio dati)
    if request.method == 'POST':
        # Creiamo un'istanza del form riempiendola con i dati dal POST
        form = HotelForm(request.POST)
        # Controlliamo se i dati sono validi
        if form.is_valid():
            hotel = form.save() # Se è valido, salviamo l'oggetto nel database!
            # 👇 2. Aggiungiamo il messaggio di successo!
            messages.success(request, f"Hotel '{hotel.nome}' creato con successo!")
            return redirect('hotel:hotel_list') # Reindirizziamo l'utente alla homepage
    
    # 3. Logica per gestire il GET (prima visita)
    else:
        # Creiamo un'istanza del form vuota
        form = HotelForm()

    # 4. Mandiamo il form (vuoto o con errori) al template
    context = {
        'form': form,
    }
    return render(request, 'gestione_hotel/hotel_create.html', context)

@permission_required('gestione_hotel.change_hotel', raise_exception=True)
def hotel_update_view(request, pk):
    queryset_sicura = Hotel.by_user.get_queryset_for_user(request.user)
    hotel = get_object_or_404(queryset_sicura, pk=pk)

    # 2. Logica per il POST (identica alla create, ma con 'instance=hotel'!)
    if request.method == 'POST':
        # Passiamo sia i dati del POST che l'istanza da modificare
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save() # Django aggiornerà l'oggetto esistente
            # Reindirizziamo alla pagina di dettaglio dell'hotel appena modificato
            # 👇 2. Aggiungiamo il messaggio di successo!
            messages.success(request, f"Hotel '{hotel.nome}' modificato con successo!")
            return redirect('hotel:hotel_detail', pk=hotel.pk)
    
    # 3. Logica per il GET (identica alla create, ma con 'instance=hotel'!)
    else:
        # Passiamo l'istanza per pre-compilare il form
        form = HotelForm(instance=hotel)

    # 4. Renderizziamo lo STESSO template della creazione!
    context = {
        'form': form,
        'hotel': hotel, # Passiamo anche l'hotel per personalizzare il titolo
    }
    return render(request, 'gestione_hotel/hotel_create.html', context)

@permission_required('gestione_hotel.delete_hotel', raise_exception=True)
def hotel_delete_view(request, pk):
    queryset_sicura = Hotel.by_user.get_queryset_for_user(request.user)
    hotel = get_object_or_404(queryset_sicura, pk=pk)

    # 2. Se la richiesta è POST, l'utente ha confermato. Cancelliamo!
    if request.method == 'POST':
        hotel.delete()
        # Reindirizziamo alla lista degli hotel dopo la cancellazione
        messages.warning(request, f"Hotel 'Hotel '{hotel.nome}' eliminato correttamente.")
        return redirect('hotel:hotel_list')
    
    # 3. Se la richiesta è GET, mostriamo la pagina di conferma
    context = {
        'hotel': hotel,
        'stanze': hotel.stanze.all(), # Già che ci siamo, puliamo anche questo
    }
    return render(request, 'gestione_hotel/hotel_confirm_delete.html', context)

def logout_view(request):
    logout(request)
    return redirect('hotel:hotel_list') # O dove preferisci


@login_required
def hotel_dashboard_view(request, pk):
    # Usiamo il nostro manager per un accesso sicuro all'hotel
    queryset_sicura = Hotel.by_user.get_queryset_for_user(request.user)
    hotel = get_object_or_404(queryset_sicura, pk=pk)

    # Prendiamo la data di oggi in modo "timezone-aware"
    oggi = timezone.now().date()

    # Query per le prenotazioni di questo hotel
    prenotazioni_hotel = hotel.prenotazioni.all()

    # 1. Arrivi di oggi
    arrivi_oggi = prenotazioni_hotel.filter(data_check_in=oggi, stato='CONFERMATA')

    # 2. Partenze di oggi
    partenze_oggi = prenotazioni_hotel.filter(data_check_out=oggi, stato='CONFERMATA')

    # 3. Ospiti attualmente in hotel (check-in <= oggi E check-out > oggi)
    ospiti_presenti = prenotazioni_hotel.filter(
        data_check_in__lte=oggi,
        data_check_out__gt=oggi,
        stato='CONFERMATA'
    )

    # Impacchettiamo tutto nel contesto
    context = {
        'hotel': hotel,
        'data_odierna': oggi,
        'arrivi_oggi': arrivi_oggi,
        'partenze_oggi': partenze_oggi,
        'ospiti_presenti': ospiti_presenti,
    }

    return render(request, 'gestione_hotel/hotel_dashboard.html', context)