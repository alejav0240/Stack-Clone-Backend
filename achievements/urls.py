from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AchievementViewSet, UserAchievementViewSet

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet)
router.register(r'user-achievements', UserAchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
