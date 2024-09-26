from django.contrib.auth import get_user_model
from rest_framework import serializers


# Get the user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        # Normalize the email
        normalized_email = value.strip().lower()
        # Check if user already exists
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return normalized_email

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Normalize the email
        return value.strip().lower()


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
