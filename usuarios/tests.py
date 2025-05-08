# usuarios/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Usuario


class UsuarioTests(APITestCase):
    def setUp(self):
        # Crear un usuario para autenticación
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Crear token para este usuario
        self.token = Token.objects.create(user=self.user)
        # Configurar la autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Crear algunos usuarios de prueba
        self.usuario1 = Usuario.objects.create(
            nombre='Usuario Test 1',
            correo='usuario1@test.com'
        )

    def test_crear_usuario(self):
        """
        Asegura que podemos crear un nuevo usuario.
        """
        url = reverse('usuario-list')
        data = {
            'nombre': 'Nuevo Usuario',
            'correo': 'nuevo@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)
        self.assertEqual(Usuario.objects.get(id=2).nombre, 'Nuevo Usuario')

    def test_listar_usuarios(self):
        """
        Asegura que podemos obtener la lista de usuarios.
        """
        url = reverse('usuario-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Verificamos paginación

    def test_buscar_por_nombre(self):
        """
        Prueba el endpoint personalizado para buscar usuarios por nombre.
        """
        # Crear más usuarios para la búsqueda
        Usuario.objects.create(nombre='María López', correo='maria@test.com')
        Usuario.objects.create(nombre='Mario Casas', correo='mario@test.com')

        url = reverse('usuario-buscar-por-nombre')
        response = self.client.get(url, {'nombre': 'Mari'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Debe encontrar 2 usuarios

    def test_sin_autenticacion(self):
        """
        Verifica que no se puede acceder sin autenticación.
        """
        # Eliminar credenciales
        self.client.credentials()
        url = reverse('usuario-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)