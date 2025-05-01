from django.test import TestCase
from ..models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='securepass123',
            name='John',
            lastname='Doe',
            rol='admin'
        )
        self.assertEqual(user.username, 'johndoe')
        self.assertTrue(user.check_password('securepass123'))
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.rol, 'admin')
        self.assertTrue(user.habilitado)
