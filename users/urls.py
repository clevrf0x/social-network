from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserSearchAPIView, UsersAPIView, CurrentUserAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('users', UsersAPIView.as_view(), name='user-list'),

    path('users/<int:pk>', UsersAPIView.as_view(), name='user-detail'),
    path('users/me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('users/search', UserSearchAPIView.as_view(), name='user_search'),
]
