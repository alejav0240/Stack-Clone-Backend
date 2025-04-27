from django.contrib import admin
from .models import UserPoint

@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'point_type', 'points', 'active')
    list_filter = ('point_type', 'active')
