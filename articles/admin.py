from django.contrib import admin
from .models import Article, Status, ArticleAudit

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    search_fields = ('title', 'body')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(ArticleAudit)
class ArticleAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'changed_at', 'change_type')
    search_fields = ('change_type',)
