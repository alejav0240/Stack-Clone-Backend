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
