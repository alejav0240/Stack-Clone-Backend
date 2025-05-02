from django.test import TestCase
from ..serializers import CustomUserSerializer
from ..models import CustomUser

class UserSerializerTest(TestCase):
    def test_valid_serializer_data(self):
        data = {
            'username': 'janedoe',
            'email': 'jane@example.com',
            'name': 'Jane',
            'lastname': 'Doe',
            'rol': 'user',
            'password': 'testpass123'
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serialized_output(self):
        user = CustomUser.objects.create_user(
            username='johndoe', email='john@example.com', password='12345',
            name='John', lastname='Doe', rol='admin'
        )
        serializer = CustomUserSerializer(user)
        self.assertEqual(serializer.data['username'], 'johndoe')
