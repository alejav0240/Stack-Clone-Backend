from rest_framework import routers
from .views import CustomUserViewSet, CookieTokenObtainPairView, RefreshAccessTokenView, LogoutView, RankViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'ranks', RankViewSet)  # Registrar el RankViewSet

urlpatterns = [
    path('', include(router.urls)),
    path('auth/create-cookie/', CookieTokenObtainPairView.as_view(), name='jwt-create-cookie'),
    path('auth/jwt/refresh-cookie/', RefreshAccessTokenView.as_view(), name='jwt-refresh-cookie'),
    path('auth/jwt/logout/', LogoutView.as_view(), name='jwt-logout'),

]
