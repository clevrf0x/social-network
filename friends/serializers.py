from rest_framework import serializers
from django.contrib.auth import get_user_model
from friends.models import FriendRequest, Friendship, BlockedUser
from users.serializer import AppUserSerializer

User = get_user_model()

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sender', 'created_at', 'updated_at']

class FriendshipSerializer(serializers.ModelSerializer):
    friend = AppUserSerializer()

    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']

class BlockedUserSerializer(serializers.ModelSerializer):
    blocked_user = AppUserSerializer()

    class Meta:
        model = BlockedUser
        fields = ['id', 'blocked_user', 'created_at']
