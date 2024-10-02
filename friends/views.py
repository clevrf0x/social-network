from django.conf import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from friends.models import FriendRequest, Friendship, BlockedUser
from friends.serializers import FriendRequestSerializer, FriendshipSerializer, BlockedUserSerializer

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FriendListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        friendships = Friendship.objects.filter(user=request.user).select_related('friend')
        
        # Apply search if query parameter is provided
        search_query = request.query_params.get('q', '')
        if search_query:
            friendships = friendships.filter(
                Q(friend__email__icontains=search_query) |
                Q(friend__first_name__icontains=search_query) |
                Q(friend__last_name__icontains=search_query)
            )
        
        friendships = friendships.order_by('friend__first_name', 'friend__last_name')
        
        paginator = self.pagination_class()
        paginated_friendships = paginator.paginate_queryset(friendships, request)
        
        serializer = FriendshipSerializer(paginated_friendships, many=True)
        return paginator.get_paginated_response(serializer.data)

class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_scope = 'friend_request'

    def post(self, request):
        receiver_id = request.data.get('receiver')
        sender = request.user

        if sender.id == receiver_id:
            return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        receiver = User.objects.filter(id=receiver_id).first()
        if not receiver:
            return Response({"detail": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)

        if BlockedUser.objects.filter(user=receiver, blocked_user=sender).exists():
            return Response({"detail": "You cannot send a friend request to this user."}, status=status.HTTP_403_FORBIDDEN)

        cache_key = f"friend_request_cooldown_{sender.id}_{receiver.id}"
        if cache.get(cache_key):
            return Response({"detail": "You cannot send a friend request to this user yet. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, status='PENDING').first()
        if existing_request:
            return Response({"detail": "A friend request to this user already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if sender.friends.filter(id=receiver.id).exists():
            return Response({"detail": "You are already friends with this user."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendRequestActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        action = request.data.get('action')
        friend_request = FriendRequest.objects.filter(id=pk, receiver=request.user).first()

        if not friend_request:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.friends.filter(id=friend_request.sender.id).exists():
            friend_request.delete()
            return Response({"detail": "You are already friends with this user. Friend request deleted."}, status=status.HTTP_200_OK)

        if action == 'accept':
            with transaction.atomic():
                friend_request.status = 'ACCEPTED'
                friend_request.save()
                Friendship.objects.create(user=friend_request.sender, friend=friend_request.receiver)
                Friendship.objects.create(user=friend_request.receiver, friend=friend_request.sender)
            return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'REJECTED'
            friend_request.save()

            # Set cooldown period
            timeout = int(os.getenv("FRIEND_REQUEST_COOLDOWN_TIMEOUT", 24 * 60 * 60))  # Default to 24 hours if not set
            cache_key = f"friend_request_cooldown_{friend_request.sender.id}_{friend_request.receiver.id}"
            cache.set(cache_key, True, timeout)

            return Response({"detail": "Friend request rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

class BlockUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user_to_block = User.objects.filter(id=user_id).first()

        if not user_to_block:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if they are friends and remove the friendship
        if request.user.friends.filter(id=user_to_block.id).exists():
            Friendship.objects.filter(user=request.user, friend=user_to_block).delete()
            Friendship.objects.filter(user=user_to_block, friend=request.user).delete()

        # Check if any pending friend requests exist and remove them
        friend_requests = FriendRequest.objects.filter(
            (Q(sender=request.user, receiver=user_to_block) | Q(sender=user_to_block, receiver=request.user)),
            status='PENDING'
        )
        if friend_requests.exists():
            friend_requests.delete()

        BlockedUser.objects.get_or_create(user=request.user, blocked_user=user_to_block)
        return Response({"detail": "User blocked successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        BlockedUser.objects.filter(user=request.user, blocked_user_id=user_id).delete()
        return Response({"detail": "User unblocked successfully."}, status=status.HTTP_200_OK)

class BlockedUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        blocked_users = BlockedUser.objects.filter(user=request.user).select_related('blocked_user')
        paginator = self.pagination_class()
        paginated_result = paginator.paginate_queryset(blocked_users, request)
        serializer = BlockedUserSerializer(paginated_result, many=True)
        return paginator.get_paginated_response(serializer.data)


class PendingFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(receiver=request.user, status='PENDING').order_by('-created_at')
        
        # Apply search if query parameter is provided
        search_query = request.query_params.get('q', '')
        if search_query:
            pending_requests = pending_requests.filter(
                Q(sender__email__icontains=search_query) |
                Q(sender__first_name__icontains=search_query) |
                Q(sender__last_name__icontains=search_query)
            )
        
        paginator = self.pagination_class()
        paginated_requests = paginator.paginate_queryset(pending_requests, request)
        
        serializer = FriendRequestSerializer(paginated_requests, many=True)
        return paginator.get_paginated_response(serializer.data)
