from django.urls import include, path

# this block overrides default html errors
from core.error_handler import handler400, handler403, handler404, handler500

from core.health_check import HealthCheckView

urlpatterns = [
    path('api/v1/healthcheck/', HealthCheckView.as_view(), name="healthcheck")
]
