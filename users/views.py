from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import CustomUser, Rank
from .serializers import CustomUserSerializer, RankSerializer, LoginUserSerializer
import logging

logger = logging.getLogger(__name__)

# 🔐 Constantes de cookies
ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,
    "samesite": "None",
}


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
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save()
        group_name = self.request.data.get('group')

        if self.request.user.is_authenticated and self.request.user.is_superuser and group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
        else:
            group, _ = Group.objects.get_or_create(name='Usuario')

        user.groups.add(group)
        logger.info(f"Usuario creado: {user.email}, Grupo asignado: {group.name}")


# 🏅 CRUD de Rangos
class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    permission_classes = [IsAdminOrForbidden]


# 🔐 Login con cookies seguras
class CookieTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning("Error en login: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "user": CustomUserSerializer(user).data
        }, status=status.HTTP_200_OK)

        response.set_cookie(ACCESS_COOKIE_NAME, access_token, **COOKIE_SETTINGS)
        response.set_cookie(REFRESH_COOKIE_NAME, str(refresh), **COOKIE_SETTINGS)
        logger.info(f"Login exitoso para el usuario: {user.email}")

        return response


# ♻️ Refrescar token usando la cookie
class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh_token:
            logger.warning("Refresh token no encontrado en cookies.")
            return Response({'detail': 'No refresh token found'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'detail': 'Access token refreshed'}, status=status.HTTP_200_OK)
            response.set_cookie(ACCESS_COOKIE_NAME, access_token, **COOKIE_SETTINGS, max_age=300)
            logger.info("Access token refrescado exitosamente.")
            return response

        except Exception as e:
            logger.error("Error al refrescar token: %s", str(e))
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


# 🔓 Logout eliminando cookies
class LogoutView(APIView):
    def post(self, request):
        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie(ACCESS_COOKIE_NAME)
        response.delete_cookie(REFRESH_COOKIE_NAME)
        logger.info("Logout exitoso.")
        return response
