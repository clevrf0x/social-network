from django.urls import path
from .views import (
    FriendRequestAPIView,
    FriendRequestActionAPIView,
    FriendListAPIView,
    BlockUserAPIView,
    BlockedUserListAPIView,
    PendingFriendRequestAPIView
)

urlpatterns = [
    path('friends', FriendListAPIView.as_view(), name='friend-list'),
    path('friends/requests', FriendRequestAPIView.as_view(), name='friend-requests'),
    path('friends/requests/pending', PendingFriendRequestAPIView.as_view(), name='pending-friend-requests'),
    path('friends/requests/<int:pk>', FriendRequestActionAPIView.as_view(), name='friend-request-action'),
    
    path('friends/block/<int:user_id>', BlockUserAPIView.as_view(), name='block-user'),
    path('friends/blocked', BlockedUserListAPIView.as_view(), name='blocked-user-list'),
]
