from faker import Faker
from .models import UserPoint

fake = Faker()

def create_user_points(users):
    for user in users:
        for point_type in ['reputation', 'contribution', 'activity']:
            UserPoint.objects.create(
                user=user,
                point_type=point_type,
                points=fake.random_int(min=0, max=1000),
            )
    print("🎉 Puntos de usuario creados exitosamente.")