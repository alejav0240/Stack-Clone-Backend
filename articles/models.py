from django.db import models
from users.models import CustomUser

class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = [
            ("approve_article", "Puede aprobar artículos"),
            ("feature_article", "Puede destacar artículos"),
        ]

    def __str__(self):
        return self.title

class ArticleAudit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    change_type = models.CharField(max_length=255)

    def __str__(self):
        return f"Change in {self.article.title} at {self.changed_at}"
