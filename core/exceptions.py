
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotFound, ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework import status

def app_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If the response is None, it means the exception was not handled by DRF
    if response is None:
        return handle_unexpected_exception(exc)

    # Handle specific exceptions
    if isinstance(exc, ValidationError):
        return handle_bad_request(exc)
    elif isinstance(exc, AuthenticationFailed):
        return handle_unauthorized()
    elif isinstance(exc, PermissionDenied):
        return handle_forbidden()
    elif isinstance(exc, NotFound):
        return handle_not_found(exc)
    elif isinstance(exc, APIException) and response.status_code == 409:
        return handle_conflict(exc)
    elif response.status_code == 429:
        return handle_rate_limit()
    elif response.status_code >= 500:
        return handle_server_error()

    return response

def handle_bad_request(exc):
    return {
        'error': {
            'type': 'bad_request',
            'message': exc.detail,
            'status': status.HTTP_400_BAD_REQUEST
        }
    }

def handle_unauthorized():
    return {
        'error': {
            'type': 'unauthorized',
            'message': 'Authentication credentials were not provided.',
            'status': status.HTTP_401_UNAUTHORIZED
        }
    }

def handle_forbidden():
    return {
        'error': {
            'type': 'forbidden',
            'message': 'You do not have permission to perform this action.',
            'status': status.HTTP_403_FORBIDDEN
        }
    }

def handle_not_found(exc):
    return {
        'error': {
            'type': 'not_found',
            'message': str(exc),
            'status': status.HTTP_404_NOT_FOUND
        }
    }

def handle_conflict(exc):
    return {
        'error': {
            'type': 'conflict',
            'message': str(exc),
            'status': status.HTTP_409_CONFLICT
        }
    }

def handle_rate_limit():
    return {
        'error': {
            'type': 'rate_limit_exceeded',
            'message': 'You have made too many requests. Please try again later.',
            'status': status.HTTP_429_TOO_MANY_REQUESTS
        }
    }

def handle_server_error():
    return {
        'error': {
            'type': 'server_error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    }

def handle_unexpected_exception(exc):
    return {
        'error': {
            'type': 'server_error',
            'message': str(exc),
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    }
