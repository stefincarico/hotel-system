# booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PrenotazioneForm
from gestione_hotel.models import Hotel

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