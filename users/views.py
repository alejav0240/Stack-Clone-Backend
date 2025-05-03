from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import CustomUser, Rank
from .serializers import CustomUserSerializer, RankSerializer, LoginUserSerializer
import logging

# Create a logger for this file
logger = logging.getLogger(__name__)

# 🔐 Permiso personalizado
class IsAdminOrForbidden(BasePermission):
    """Permite el acceso solo a administradores (staff)."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# 👤 CRUD de Usuarios
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []  # El registro no requiere autenticación
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save()
        group_name = self.request.data.get('group', 'Usuario')  # Grupo por defecto: "Usuario"

        # Si el request.user es superusuario, permite asignar cualquier grupo
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            group, _ = Group.objects.get_or_create(name=group_name)
        else:
            group, _ = Group.objects.get_or_create(name='Usuario')

        user.groups.add(group)

# 🏅 CRUD de Rangos
class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    permission_classes = [IsAdminOrForbidden]

# 🔐 Login con cookies seguras
class CookieTokenObtainPairView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "user": CustomUserSerializer(user).data},
                status=status.HTTP_200_OK)

            response.set_cookie(key="access_token",
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")

            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # ♻️ Refrescar token usando la cookie
class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'No refresh token found'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            res = Response({'detail': 'Access token refreshed'}, status=status.HTTP_200_OK)
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # Changed to True
                samesite='Lax',
                max_age=300  # 5 minutes
            )
            return res
        except Exception:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

# 🔓 Logout eliminando cookies
class LogoutView(APIView):
    def post(self, request):
        res = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res
