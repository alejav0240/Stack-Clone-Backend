from rest_framework import routers
from .views import CustomUserViewSet, CookieTokenObtainPairView, RefreshAccessTokenView, LogoutView
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('auth/jwt/create/', CookieTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh-cookie/', RefreshAccessTokenView.as_view(), name='jwt-refresh-cookie'),
    path('auth/jwt/logout/', LogoutView.as_view(), name='jwt-logout'),

]
