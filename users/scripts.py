from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker

from .models import Rank

fake = Faker()

def create_test_users():
    User = get_user_model()

    test_users = {
        'admin_user': 'Administrador',
        'moderator_user': 'Moderador',
        'author_user': 'Autor',
        'normal_user': 'Usuario',
        'reviewer_user': 'Revisor de Contenido',
        'editor_user': 'Editor de Artículos',
    }

    for username, group_name in test_users.items():
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='Password'  # 👈 Cambia la contraseña si quieres
            )
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            user.save()
        else:
            print(f"⚠️ Usuario '{username}' ya existe.")

def create_fake_users(count=50):
    User = get_user_model()
    created_users = []  # Lista para almacenar los usuarios creados

    try:
        user_group = Group.objects.get(name='Usuario')
    except Group.DoesNotExist:
        print("❌ El grupo 'Usuario' no existe. Corre primero las señales para crear grupos.")
        return created_users  # Retorna una lista vacía si el grupo no existe

    for _ in range(count):
        username = fake.user_name() + str(fake.random_int(min=1000, max=9999))
        email = fake.email()
        password = 'TestPassword123'  # Mismo password para todos los fake

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.groups.add(user_group)
            user.save()
            created_users.append(user)  # Agrega el usuario creado a la lista
        else:
            print(f"⚠️ Usuario {username} ya existía, saltado.")

    print(f"🎉 {len(created_users)} usuarios falsos creados exitosamente.")
    # Retorna una lista vacía si no se crearon usuarios
    return created_users  # Retorna la lista de usuarios creados

def create_ranks():
    for level in range(1, 11):  # Niveles del 1 al 10
        name = f"Nivel {level}"
        min_points = level * 100  # Ejemplo: 100 puntos por nivel
        Rank.objects.get_or_create(name=name, min_points=min_points)
    print("🎉 Ranks creados exitosamente.")