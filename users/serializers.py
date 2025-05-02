from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import CustomUser, Rank

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    rank = RankSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'age', 'rol','rank', 'habilitado', 'created_at')
        read_only_fields = ('id', 'created_at')


class CustomUserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """Validar que el correo electrónico sea único."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def create(self, validated_data):
        """Crear un usuario con un grupo predeterminado."""
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        # Asignar el grupo "Usuario" por defecto
        user_group, _ = Group.objects.get_or_create(name='Usuario')
        user.groups.add(user_group)
        return user

class LoginUserSerializer(Serializer):
    username = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")