from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
# Registra aquí los ViewSets de diferentes aplicaciones si es un router global
# router.register(r'users', users_views.UserViewSet, basename='user')
# router.register(r'questions', questions_views.QuestionViewSet, basename='question')
# ...

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include([
        path('', include(router.urls)),
        path('auth/', include('rest_framework.urls', namespace='rest_framework')),
        # path('users/', include('users.urls')),
        # path('questions/', include('questions.urls')),
        # path('articles/', include('articles.urls')),
        # path('achievements/', include('achievements.urls')),
    ])),
]