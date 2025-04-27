from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Rank

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_points')
    search_fields = ('name',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Aquí defines qué campos mostrar en el listado del Admin
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'habilitado', 'is_staff']
    list_filter = ['rol', 'habilitado', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'age', 'rol', 'habilitado')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'age', 'rol', 'habilitado'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('id',)
