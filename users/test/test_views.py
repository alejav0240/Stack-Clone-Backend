from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from django.contrib.auth.models import Group

class UserViewSetTest(APITestCase):
    def setUp(self):
        # Crear usuarios para las pruebas
        self.user = CustomUser.objects.create_user(
            username='user1', email='user1@example.com', password='pass1234'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass'
        )
        self.login_url = reverse('jwt-create-cookie')
        self.user_list_url = reverse('customuser-list')  # Endpoint para listar usuarios
        self.user_detail_url = lambda user_id: reverse('customuser-detail', args=[user_id])  # Definir la URL de detalle

    def authenticate(self, username, password):
        """Helper para autenticar y obtener un token."""
        response = self.client.post(self.login_url, {
            'username': username,
            'password': password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error en login: {response.data}")
        token = response.data.get('access')
        self.assertIsNotNone(token, "El token de acceso no fue generado.")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_user_login(self):
        """Probar el login de un usuario."""
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error en login: {response.data}")
        self.assertIn('access', response.data)

    def test_unauthorized_user_list(self):
        """Probar que un usuario no autenticado no puede listar usuarios."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "La vista no está protegida correctamente con permisos.")

    def test_authorized_user_list(self):
        """Probar que un usuario autenticado puede listar usuarios."""
        self.authenticate('admin', 'adminpass')
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "El usuario autenticado no pudo acceder a la lista de usuarios.")

    def test_create_user(self):
        """Probar la creación de un usuario."""
        self.authenticate('admin', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "No se pudo crear el usuario.")
        self.assertEqual(response.data['username'], 'newuser')

    def test_update_user(self):
        """Probar la actualización de un usuario."""
        self.authenticate('admin', 'adminpass')
        user_detail_url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.patch(user_detail_url, {
            'email': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, "No se pudo actualizar el usuario.")
        self.assertEqual(response.data['email'], 'updateduser@example.com')

    def test_delete_user(self):
        """Probar la eliminación de un usuario."""
        self.authenticate('admin', 'adminpass')
        user_detail_url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.delete(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, "No se pudo eliminar el usuario.")
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())

    def test_retrieve_user(self):
        """Probar que un usuario autenticado puede obtener los detalles de un usuario."""
        self.authenticate('admin', 'adminpass')
        response = self.client.get(self.user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK, "No se pudo obtener el detalle del usuario.")
        self.assertEqual(response.data['username'], self.user.username)

    def test_non_admin_cannot_create_user(self):
        """Probar que un usuario no administrador puede registrarse."""
        self.authenticate('user1', 'pass1234')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,"Un usuario no administrador no pudo registrarse.")
        self.assertEqual(response.data['username'], 'newuser')

    def test_admin_can_create_user_with_moderator_group(self):
        """Probar que un administrador puede crear usuarios con el grupo Moderador."""
        self.authenticate('admin', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'group': 'Moderador'  # Especificar el grupo Moderador en la solicitud
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "El administrador no pudo crear un usuario.")
        self.assertEqual(response.data['username'], 'newuser')

        # Verificar que el usuario pertenece al grupo Moderador
        new_user = CustomUser.objects.get(username='newuser')
        moderator_group = Group.objects.get(name='Moderador')
        self.assertIn(moderator_group, new_user.groups.all(), "El usuario no fue asignado al grupo Moderador.")

    def test_invalid_user_creation(self):
        """Probar que no se pueden crear usuarios con datos inválidos."""
        self.authenticate('admin', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': '',
            'email': 'invalidemail',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Se permitió crear un usuario con datos inválidos.")

    def test_rank_viewset_access(self):
        """Probar acceso al endpoint de RankViewSet sin permisos."""
        self.authenticate('user1', 'pass1234')
        rank_list_url = reverse('rank-list')
        response = self.client.get(rank_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "El endpoint RankViewSet no está protegido correctamente.")

    def test_cookie_token_obtain(self):
        """Probar que las cookies se establecen correctamente al iniciar sesión."""
        response = self.client.post(self.login_url, {
            'email': 'user1@example.com',
            'password': 'pass1234'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Error en login.")

        set_cookie = response.headers.get('Set-Cookie', '')
        print("set Cokies",set_cookie)

        print("Response cookies:", response.cookies)
        
        # Check if cookies exist
        self.assertTrue('access_token' in response.cookies, "Access token cookie not set")
        self.assertTrue('refresh_token' in response.cookies, "Refresh token cookie not set")
        
        # Check cookie attributes
        access_cookie = response.cookies['access_token']
        self.assertTrue(access_cookie['httponly'], "Access token cookie should be httponly")
        self.assertTrue(access_cookie['secure'], "Access token cookie should be secure")

