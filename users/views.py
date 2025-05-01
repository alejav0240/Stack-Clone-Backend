from rest_framework import viewsets
from .models import CustomUser, Rank
from .serializers import CustomUserSerializer, RankSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data['access']
            refresh = response.data['refresh']

            res = Response({"detail": "Login successful"}, status=status.HTTP_200_OK)

            # Setear cookies
            res.set_cookie(
                key='access_token',
                value=access,
                httponly=True,
                secure=True,  # solo HTTPS en producción
                samesite='Lax',
                max_age=60 * 5,  # 5 minutos
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=60 * 60 * 24 * 7,  # 7 días
            )

            return res

        return response
class RefreshAccessTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'detail': 'No refresh token'}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            res = Response({'detail': 'Access refreshed'})
            res.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax', max_age=300)
            return res
        except Exception:
            return Response({'detail': 'Invalid refresh token'}, status=401)

class LogoutView(APIView):
    def post(self, request):
        res = Response({'detail': 'Logout successful'})
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res