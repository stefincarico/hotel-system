# gestione_hotel/views.py

from django.shortcuts import get_object_or_404, render,redirect
from .models import Hotel, Stanza
from .forms import HotelForm # 👈 1. Importiamo il modello Hotel
from django.contrib.auth.decorators import login_required # 👈 1. Importiamo il decoratore
from django.contrib.auth import logout
from django.contrib import messages 
from .decorators import custom_login_required
from django.contrib.auth.decorators import permission_required

# Create your views here.

@login_required
def homepage_view(request):
    # Se l'utente è un superuser, può vedere tutto!
    if request.user.is_superuser:
        lista_hotel_attivi = Hotel.objects.filter(stato=Hotel.StatoHotel.ATTIVO).order_by('nome')
    else:
        # Altrimenti, filtriamo gli hotel dalla lista del suo profilo!
        lista_hotel_attivi = request.user.userprofile.allowed_hotels.filter(
            stato=Hotel.StatoHotel.ATTIVO
        ).order_by('nome')

    context = {
        'hotels': lista_hotel_attivi,
    }
    return render(request, 'gestione_hotel/homepage.html', context)

@login_required
def hotel_detail_view(request, pk):
    # PRIMA di fare qualsiasi altra cosa, controlliamo se l'utente ha accesso a questo hotel.
    # Se l'utente non è superuser, cerchiamo l'hotel SOLO tra quelli a lui permessi.
    if request.user.is_superuser:
        hotel = get_object_or_404(Hotel, pk=pk)
    else:
        hotel = get_object_or_404(request.user.userprofile.allowed_hotels, pk=pk)

    # Il resto della view funziona come prima, perché abbiamo già l'hotel giusto!
    stanze_dell_hotel = hotel.stanze.all()
    context = {
        'hotel': hotel,
        'stanze': stanze_dell_hotel,
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

@login_required
def hotel_update_view(request, pk):
    if request.user.is_superuser:
        hotel = get_object_or_404(Hotel, pk=pk)
    else:
        hotel = get_object_or_404(request.user.userprofile.allowed_hotels, pk=pk)

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

@login_required
def hotel_delete_view(request, pk):
    if request.user.is_superuser:
        hotel = get_object_or_404(Hotel, pk=pk)
    else:
        hotel = get_object_or_404(request.user.userprofile.allowed_hotels, pk=pk)

    # 2. Se la richiesta è POST, l'utente ha confermato. Cancelliamo!
    if request.method == 'POST':
        hotel.delete()
        # Reindirizziamo alla lista degli hotel dopo la cancellazione
        messages.warning(request, f"Hotel 'Hotel '{hotel.nome}' eliminato correttamente.")
        return redirect('hotel:hotel_list')

    # 3. Se la richiesta è GET, mostriamo la pagina di conferma
    context = {
        'hotel': hotel
    }
    return render(request, 'gestione_hotel/hotel_confirm_delete.html', context)

def logout_view(request):
    logout(request)
    return redirect('hotel:hotel_list') # O dove preferisci