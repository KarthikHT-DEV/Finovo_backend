from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, ProfileSerializer
from .models import UserProfile

User = get_user_model()


class LoginView(APIView):
    """
    POST /api/auth/login/

    Accepts { email, password } and returns JWT access + refresh tokens
    along with basic user profile data.
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email    = serializer.validated_data['email']
        password = serializer.validated_data['password']

        from django.contrib.auth import authenticate

        # CustomUser uses email as USERNAME_FIELD
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'No account found with this email address.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        authenticated_user = authenticate(
            request, email=user.email, password=password
        )
        if authenticated_user is None:
            return Response(
                {'error': 'Incorrect password. Please try again.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(authenticated_user)
        return Response(
            {
                'access':  str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id':         authenticated_user.id,
                    'email':      authenticated_user.email,
                    'first_name': authenticated_user.first_name,
                    'last_name':  authenticated_user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    """
    POST /api/auth/register/

    Accepts { full_name, email, password }.
    Creates a new user and immediately returns JWT tokens so the user
    is logged in right after registration.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data['full_name'].strip()
        email     = serializer.validated_data['email']
        password  = serializer.validated_data['password']

        # Split full name into first / last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name  = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access':  str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id':         user.id,
                    'email':      user.email,
                    'first_name': user.first_name,
                    'last_name':  user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    """
    GET  /api/users/profile/  — returns the authenticated user's profile
    PATCH /api/users/profile/ — updates first_name, last_name, monthly_savings_goal
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def _get_or_create_profile(self, user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        user = request.user
        profile = self._get_or_create_profile(user)
        serializer = ProfileSerializer(
            {'user': user, 'profile': profile}
        )
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        profile = self._get_or_create_profile(user)

        data = request.data
        print(f"DEBUG: Profile update for {user.email}")
        print(f"DEBUG: Received data keys: {list(data.keys())}")
        print(f"DEBUG: Received files: {list(request.FILES.keys())}")

        # Update user fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            new_email = data['email'].strip().lower()
            # Only update if different; skip if already taken by another user
            if new_email and new_email != user.email:
                if User.objects.filter(email__iexact=new_email).exclude(pk=user.pk).exists():
                    return Response(
                        {'error': 'Email already in use by another account.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.email = new_email
        user.save()

        # Update profile fields
        if 'monthly_savings_goal' in data:
            try:
                profile.monthly_savings_goal = Decimal(str(data['monthly_savings_goal']))
            except Exception:
                return Response(
                    {'error': 'Invalid savings goal value.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if 'phone_number' in data:
            profile.phone_number = data['phone_number']
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()

        serializer = ProfileSerializer({'user': user, 'profile': profile})
        return Response(serializer.data)
