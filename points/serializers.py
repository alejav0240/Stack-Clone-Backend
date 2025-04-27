from rest_framework import serializers
from .models import UserPoint

class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = '__all__'
