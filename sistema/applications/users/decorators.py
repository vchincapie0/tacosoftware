from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_admin:
            # Si el usuario no es administrador, mostrar un mensaje de error y redirigir a la página de inicio
            messages.error(request, 'Acceso denegado. No tienes permisos para acceder a esta página.')
            return redirect('home_app:home')  # Reemplaza 'home_app:home' con la URL de la página de inicio

        # Si el usuario es administrador o está autenticado, ejecutar la vista normalmente
        return view_func(request, *args, **kwargs)

    return wrapped_view