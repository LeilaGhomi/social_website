from django.shortcuts import redirect
from django.contrib import messages

LOGIN_EXEMPT_URLS = [
    'admin/',
    '/',
    '/register/',
]


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in LOGIN_EXEMPT_URLS:
            messages.error(request, 'You should login first!', 'warning')
            return redirect('/')
        response = self.get_response(request)
        return response
