from django.contrib import admin
from .models import Tag, QuestionTag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active')
    search_fields = ('name',)
    list_filter = ('active',)

@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    list_display = ('question', 'tag', 'active')
    list_filter = ('active',)
