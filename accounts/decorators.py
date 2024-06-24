# decorators.py

from django.http import HttpResponse

def cors(methods=None):
    """
    Custom CORS decorator.
    Adds CORS headers to the response for specified HTTP methods.
    """

    allowed_methods = methods if methods else []

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if request.method in allowed_methods:
                # Add CORS headers as needed
                response['Access-Control-Allow-Origin'] = '*'  # Example: Allow all origins
                response['Access-Control-Allow-Methods'] = ','.join(allowed_methods)
                response['Access-Control-Allow-Headers'] = 'Content-Type'

            return response

        return wrapper

    return decorator
