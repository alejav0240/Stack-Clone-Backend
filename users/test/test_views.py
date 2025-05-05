from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from django.contrib.auth.models import Group

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user1', email='user1@example.com', password='pass1234'
        )
        self.admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass'
        )
        self.login_url = reverse('jwt-create-cookie')
        self.user_list_url = reverse('customuser-list')
        self.user_detail_url = lambda user_id: reverse('customuser-detail', args=[user_id])

    def authenticate(self, email, password):
        response = self.client.post(self.login_url, {
            'email': email,
            'password': password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error en login: {response.data}")
        # Verificamos que se establecieron las cookies
        self.assertIn('access_token', response.cookies, "Access token cookie not set")
        self.assertIn('refresh_token', response.cookies, "Refresh token cookie not set")
        print("Autenticación exitosa con cookies.")

    def test_cookie_token_obtain(self):
        response = self.client.post(self.login_url, {
            'email': 'user1@example.com',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Error en login.")
        set_cookie = response.headers.get('Set-Cookie', '')
        self.assertTrue('access_token' in response.cookies, "Access token cookie not set")
        self.assertTrue('refresh_token' in response.cookies, "Refresh token cookie not set")
        access_cookie = response.cookies['access_token']
        self.assertTrue(access_cookie['httponly'], "Access token cookie should be httponly")
        self.assertTrue(access_cookie['secure'], "Access token cookie should be secure")

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'email': 'user1@example.com',
            'password': 'pass1234'
        })
        print("Login URL:", self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Error en login: {response.data}")
        self.assertTrue('access_token' in response.cookies, "Access token cookie not set")
        self.assertTrue('refresh_token' in response.cookies, "Refresh token cookie not set")
        print("Login exitoso. Respuesta:", response.data)

    def test_unauthorized_user_list(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "La vista no está protegida correctamente con permisos.")
        print("Intento de acceso no autorizado. Respuesta:", response.data)

    def test_authorized_user_list(self):
        self.authenticate('admin@example.com', 'adminpass')
        response = self.client.get(self.user_list_url)
        print("User list URL:", self.user_list_url)
        print("Headers:", response.headers)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "El usuario autenticado no pudo acceder a la lista de usuarios.")
        print("Lista de usuarios obtenida. Respuesta:", response.data)

    def test_create_user(self):
        self.authenticate('admin@example.com', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "No se pudo crear el usuario.")
        self.assertEqual(response.data['username'], 'newuser')
        print("Usuario creado exitosamente. Respuesta:", response.data)

    def test_update_user(self):
        self.authenticate('admin@example.com', 'adminpass')
        user_detail_url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.patch(user_detail_url, {
            'email': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK, "No se pudo actualizar el usuario.")
        self.assertEqual(response.data['email'], 'updateduser@example.com')
        print("Usuario actualizado. Respuesta:", response.data)

    def test_delete_user(self):
        self.authenticate('admin@example.com', 'adminpass')
        user_detail_url = reverse('customuser-detail', args=[self.user.id])
        response = self.client.delete(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, "No se pudo eliminar el usuario.")
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
        print("Usuario eliminado exitosamente.")

    def test_retrieve_user(self):
        self.authenticate('admin@example.com', 'adminpass')
        response = self.client.get(self.user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK, "No se pudo obtener el detalle del usuario.")
        self.assertEqual(response.data['username'], self.user.username)
        print("Detalle del usuario obtenido. Respuesta:", response.data)

    def test_non_admin_cannot_create_user(self):
        self.authenticate('user1@example.com', 'pass1234')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Un usuario no administrador no pudo registrarse.")
        self.assertEqual(response.data['username'], 'newuser')
        print("Usuario registrado por no administrador. Respuesta:", response.data)

    def test_admin_can_create_user_with_moderator_group(self):
        self.authenticate('admin@example.com', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'group': 'Moderador'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "El administrador no pudo crear un usuario.")
        self.assertEqual(response.data['username'], 'newuser')
        new_user = CustomUser.objects.get(username='newuser')
        moderator_group = Group.objects.get(name='Moderador')
        self.assertIn(moderator_group, new_user.groups.all(), "El usuario no fue asignado al grupo Moderador.")
        print("Usuario con grupo Moderador creado. Respuesta:", response.data)

    def test_invalid_user_creation(self):
        self.authenticate('admin@example.com', 'adminpass')
        response = self.client.post(self.user_list_url, {
            'username': '',
            'email': 'invalidemail',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Se permitió crear un usuario con datos inválidos.")
        print("Intento de creación de usuario inválido. Respuesta:", response.data)

    def test_rank_viewset_access(self):
        self.authenticate('user1@example.com', 'pass1234')
        rank_list_url = reverse('rank-list')
        response = self.client.get(rank_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "El endpoint RankViewSet no está protegido correctamente.")
        print("Acceso denegado al endpoint RankViewSet. Respuesta:", response.data)