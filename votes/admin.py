from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vote_type', 'created_at', 'question', 'answer', 'article')
    list_filter = ('vote_type',)
