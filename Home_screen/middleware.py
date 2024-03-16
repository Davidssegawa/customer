# middleware.py

from django.http import HttpResponseNotFound

class DisableFaviconMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the favicon.ico file
        if request.path == '/favicon.ico':
            # Return a 404 Not Found response
            return HttpResponseNotFound()

        # Continue with the request processing
        return self.get_response(request)
