from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserSearchAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('users/search', UserSearchAPIView.as_view(), name='user_search')
]
