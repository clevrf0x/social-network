from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializer import RegisterSerializer, LoginSerializer, AppUserSerializer

# Get the user model
User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'email': user.email, 
                'first_name': user.first_name, 
                'last_name': user.last_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email).first()
            
            if user and user.check_password(password):
                # Update last_login
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])

                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    class UserSearchPagination(PageNumberPagination):
        page_size = 10

    def get(self, request):
        search_query = request.query_params.get('q', '')
        
        if not search_query:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for exact email match first
        exact_email_match = User.objects.filter(email__iexact=search_query).first()
        if exact_email_match:
            serializer = AppUserSerializer(exact_email_match)
            return Response(serializer.data)

        # Perform full-text search on name fields
        vector = SearchVector('first_name', 'last_name')
        query = SearchQuery(search_query)
        
        users = User.objects.annotate(
            search=vector,
            rank=SearchRank(vector, query)
        ).filter(
            Q(search=query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        ).order_by('-rank')

        # Apply pagination
        paginator = self.UserSearchPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        
        serializer = AppUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
