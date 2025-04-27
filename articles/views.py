from rest_framework import viewsets
from .models import Article, Status, ArticleAudit
from .serializers import ArticleSerializer, StatusSerializer, ArticleAuditSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ArticleAuditViewSet(viewsets.ModelViewSet):
    queryset = ArticleAudit.objects.all()
    serializer_class = ArticleAuditSerializer
