from rest_framework.test import APITestCase
from rest_framework import permissions
from ..models import CustomUser
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Permiso que permite acceso de solo lectura a usuarios no administradores,
    y acceso completo a administradores.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class UserPermissionsTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='pass', email='a@a.com')
        self.admin = CustomUser.objects.create_superuser(username='admin', password='adminpass', email='b@b.com')

    def test_is_admin_permission(self):
        request = self.client.get('/api/users/')
        permission = IsAdminOrReadOnly()
        request.user = self.admin
        self.assertTrue(permission.has_permission(request, None))

        request.user = self.user
        self.assertFalse(permission.has_permission(request, None))
