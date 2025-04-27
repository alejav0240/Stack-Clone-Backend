from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VoteViewSet

router = DefaultRouter()
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
