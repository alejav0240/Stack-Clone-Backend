from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'active')
    search_fields = ('title', 'body')
    list_filter = ('active',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user', 'created_at', 'active')
    search_fields = ('body',)
    list_filter = ('active',)
