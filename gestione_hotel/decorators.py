# gestione_hotel/decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def custom_login_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Devi effettuare il login per accedere a questa pagina.")
            # La logica di reindirizzamento è gestita da user_passes_test
            # che si comporta come login_required se il test fallisce.
            decorated_view = user_passes_test(
                lambda u: u.is_authenticated,
            )(function)
            return decorated_view(request, *args, **kwargs)
        return function(request, *args, **kwargs)
    
    return wrapper