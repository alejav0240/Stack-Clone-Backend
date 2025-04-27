from rest_framework import serializers
from .models import Article, Status, ArticleAudit

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

class ArticleAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleAudit
        fields = '__all__'
