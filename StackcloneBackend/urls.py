from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

# Rutas de autenticación
auth_patterns = [
    path('', include('djoser.urls')),  # Endpoints de djoser (register, reset password, etc)
    path('', include('djoser.urls.jwt')),  # Endpoints de JWT
    path('', include('rest_framework.urls', namespace='rest_framework')),  # Navegador de API de DRF
]

# Rutas de la API principal
api_patterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
    path('', include('users.urls')),
    path('', include('questions.urls')),
    path('', include('articles.urls')),
    path('', include('achievements.urls')),
]

# Rutas principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]