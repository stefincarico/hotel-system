# booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PrenotazioneForm
from gestione_hotel.models import Hotel
from .models import Prenotazione
from django.core.exceptions import PermissionDenied


@login_required
def prenotazione_create_view(request, hotel_pk):
    # L'utente può creare prenotazioni solo per gli hotel a cui è autorizzato
    queryset_sicura = Hotel.by_user.get_queryset_for_user(request.user)
    hotel = get_object_or_404(queryset_sicura, pk=hotel_pk)

    if request.method == 'POST':
        form = PrenotazioneForm(request.POST, hotel=hotel)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.hotel = hotel # Impostiamo l'hotel automaticamente
            prenotazione.save()
            messages.success(request, "Prenotazione creata con successo!")
            return redirect('hotel:hotel_detail', pk=hotel.pk)
    else:
        form = PrenotazioneForm(hotel=hotel)

    context = {
        'form': form,
        'hotel': hotel,
    }
    return render(request, 'booking/prenotazione_form.html', context)

@login_required
def prenotazione_update_view(request, pk):
    # Recuperiamo la prenotazione, ma assicuriamoci che l'utente possa modificarla
    # (cioè che appartenga a un hotel a cui ha accesso)
    prenotazione = get_object_or_404(Prenotazione, pk=pk)
    hotel = prenotazione.hotel
    
    # Controllo di sicurezza: l'utente può accedere a questo hotel?
    if not request.user.is_superuser and hotel not in request.user.userprofile.allowed_hotels.all():
        raise PermissionDenied("Non hai il permesso di modificare prenotazioni per questo hotel.")

    if request.method == 'POST':
        form = PrenotazioneForm(request.POST, instance=prenotazione, hotel=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Prenotazione modificata con successo!")
            # Torniamo al dettaglio dell'hotel a cui appartiene la prenotazione
            return redirect('hotel:hotel_detail', pk=hotel.pk)
    else:
        form = PrenotazioneForm(instance=prenotazione, hotel=hotel)

    context = {
        'form': form,
        'hotel': hotel,
        'prenotazione': prenotazione, # Lo passiamo per personalizzare il template
    }
    return render(request, 'booking/prenotazione_form.html', context)


@login_required
def prenotazione_cancel_view(request, pk):
    prenotazione = get_object_or_404(Prenotazione, pk=pk)
    hotel = prenotazione.hotel

    # Controllo di sicurezza
    if not request.user.is_superuser and hotel not in request.user.userprofile.allowed_hotels.all():
        raise PermissionDenied

    if request.method == 'POST':
        # Non cancelliamo, cambiamo lo stato!
        prenotazione.stato = Prenotazione.StatoPrenotazione.CANCELLATA
        prenotazione.save()
        messages.warning(request, "La prenotazione è stata annullata.")
        return redirect('hotel:hotel_detail', pk=hotel.pk)
    
    context = {
        'prenotazione': prenotazione,
        'hotel': hotel,
    }
    return render(request, 'booking/prenotazione_cancel_confirm.html', context)