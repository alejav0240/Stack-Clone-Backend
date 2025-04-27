from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ArticleViewSet, ArticleAuditViewSet, StatusViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'article-audits', ArticleAuditViewSet)

router.register(r'status', StatusViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
