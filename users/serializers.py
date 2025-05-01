from rest_framework import serializers
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
        """Crear un usuario con contraseña encriptada."""
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )