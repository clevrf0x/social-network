from django.http import JsonResponse
from django.conf import settings

def handler400(request, exception):
    return JsonResponse({
        'error': {
            'type': 'bad_request',
            'message': 'Bad request',
            'status': 400
        }
    }, status=400)

def handler403(request, exception):
    return JsonResponse({
        'error': {
            'type': 'forbidden',
            'message': 'You do not have permission to perform this action',
            'status': 403
        }
    }, status=403)

def handler404(request, exception):
    return JsonResponse({
        'error': {
            'type': 'not_found',
            'message': 'The requested resource was not found',
            'status': 404
        }
    }, status=404)

def handler500(request):
    return JsonResponse({
        'error': {
            'type': 'server_error',
            'message': 'An unexpected error occurred',
            'status': 500
        }
    }, status=500)
