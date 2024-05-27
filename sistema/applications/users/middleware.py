import threading

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Almacenar el usuario actual en un atributo de contexto
        threading.current_user = request.user
        response = self.get_response(request)
        return response