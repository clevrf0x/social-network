from django.urls import include, path

# this block overrides default html errors
from core.error_handler import handler400, handler403, handler404, handler500

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from core.health_check import HealthCheckView

urlpatterns = [
    path('api/v1/healthcheck', HealthCheckView.as_view(), name="healthcheck"),
    path('api/v1/', include('users.urls')),
    path('api/v1/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
