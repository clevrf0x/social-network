import logging
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector
from django.db.models import Q, Exists, OuterRef
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from friends.models import BlockedUser
from users.serializer import RegisterSerializer, LoginSerializer, AppUserSerializer

logger = logging.getLogger()
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
        logger.info(f"User {user} registered succefully")
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
            logger.info(f"Invalid login attempt for {user}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UsersAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsStaffUser()]
        elif self.request.method in ['DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
                serializer = AppUserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                raise NotFound(detail="User not found")
        else:
            # If the user is not staff or admin, exclude blocked users
            users = User.objects.all()
            if not request.user.is_staff and not request.user.is_superuser:
                blocked_by_users = BlockedUser.objects.filter(blocked_user=request.user).values_list('user', flat=True)
                users = users.exclude(id__in=blocked_by_users)

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(users, request)
            
            if page is not None:
                serializer = AppUserSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        
        serializer = AppUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
        
        serializer = AppUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
        
        serializer = AppUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AppUserSerializer(request.user)
        return Response(serializer.data)


class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        search_query = request.query_params.get('q', '')
        
        if not search_query:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        # Subquery to check if the logged-in user is blocked
        blocked_subquery = BlockedUser.objects.filter(
            user=OuterRef('pk'),
            blocked_user=request.user
        )

        # Check for exact email match first
        exact_email_match = User.objects.annotate(
            is_blocked=Exists(blocked_subquery)
        ).filter(
            email__iexact=search_query,
            is_blocked=False
        ).first()

        if exact_email_match:
            serializer = AppUserSerializer(exact_email_match)
            return Response(serializer.data)

        # Perform full-text search on name fields
        vector = SearchVector('first_name', 'last_name')
        query = SearchQuery(search_query)
        
        users = User.objects.annotate(
            search=vector,
            rank=SearchRank(vector, query),
            is_blocked=Exists(blocked_subquery)
        ).filter(
            (Q(search=query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)) &
            Q(is_blocked=False)
        ).order_by('-rank')

        # Pagination
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        
        serializer = AppUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
