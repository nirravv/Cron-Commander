from django.http import HttpResponse
from functools import wraps

def cors(methods=None):
    """
    Custom CORS decorator.
    Adds CORS headers to the response for specified HTTP methods.
    """

    allowed_methods = methods if methods else []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Pre-flight response for OPTIONS request
            if request.method == 'OPTIONS':
                response = HttpResponse()
                response['Access-Control-Allow-Origin'] = '*'
                response['Access-Control-Allow-Methods'] = ','.join(allowed_methods)
                response['Access-Control-Allow-Headers'] = 'Content-Type'
                return response

            response = view_func(request, *args, **kwargs)

            # Add CORS headers to the actual response
            if request.method in allowed_methods:
                response['Access-Control-Allow-Origin'] = '*'
                response['Access-Control-Allow-Methods'] = ','.join(allowed_methods)
                response['Access-Control-Allow-Headers'] = 'Content-Type'

            return response

        return wrapper

    return decorator
