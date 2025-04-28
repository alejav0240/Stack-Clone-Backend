from faker import Faker
from .models import Achievement, UserAchievement

fake = Faker()

def create_achievements(count=10):
    achievements = []
    for _ in range(count):
        achievement = Achievement.objects.create(
            name=fake.word().capitalize(),
            description=fake.sentence(nb_words=6),
        )
        achievements.append(achievement)
    print(f"🎉 {len(achievements)} Logros creados exitosamente.")
    return achievements

def assign_user_achievements(users, achievements):
    for user in users:
        achieved = fake.random_elements(achievements, length=fake.random_int(min=0, max=len(achievements)))
        for achievement in achieved:
            UserAchievement.objects.create(
                user=user,
                achievement=achievement,
            )
    print("🎉 Logros de usuario asignados exitosamente.")