from django.db import models
from users.models import CustomUser

class UserPoint(models.Model):
    POINT_TYPES = [
        ('reputation', 'Reputation'),
        ('contribution', 'Contribution'),
        ('activity', 'Activity'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    point_type = models.CharField(max_length=20, choices=POINT_TYPES)
    points = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.points} points of {self.point_type} for {self.user.username}"
