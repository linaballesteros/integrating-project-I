from django.shortcuts import redirect
from django.urls import reverse

class MiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Tu lógica de middleware aquí

        if not request.user.is_authenticated and request.path != '/accounts/login/':
            # Si el usuario no está autenticado y no está intentando acceder a la página de inicio de sesión,
            # redirige a la página de inicio de sesión
            return redirect('accounts:login')
        
        response = self.get_response(request)
        return response
