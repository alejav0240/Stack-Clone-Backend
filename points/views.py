from rest_framework import viewsets
from .models import UserPoint
from .serializers import UserPointSerializer

class UserPointViewSet(viewsets.ModelViewSet):
    queryset = UserPoint.objects.all()
    serializer_class = UserPointSerializer
