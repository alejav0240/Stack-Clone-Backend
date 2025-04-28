from rest_framework import viewsets
from .models import Article, Status, ArticleAudit
from .serializers import ArticleSerializer, StatusSerializer, ArticleAuditSerializer
from django.contrib.auth.decorators import permission_required

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ArticleAuditViewSet(viewsets.ModelViewSet):
    queryset = ArticleAudit.objects.all()
    serializer_class = ArticleAuditSerializer

@permission_required('articles.can_approve_article')
def approve_article(request, article_id):
    # Solo usuarios con permiso pueden entrar aquí
    ...
