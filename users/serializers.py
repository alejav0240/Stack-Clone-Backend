from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'age', 'rol', 'habilitado', 'created_at')
        read_only_fields = ('id', 'created_at')
