from django.test import TestCase
from applications.users.models import User
from applications.users.forms import UserRegisterForm, UserUpdateForm
from django.urls import reverse

User = User

#Requermiento 1.1
class UserManagerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)
        # Crea un usuario superusuario para usar en UserAudit si es necesario
        self.superuser = User.objects.create_superuser(
            name='Admin',
            last_name='User',
            username='adminuser',
            password='adminpassword123'
        )

    def test_create_user(self):
        user = User.objects.create_user(
            name='Another',
            last_name='User',
            username='anotheruser',
            password='password123'
        )
        self.assertEqual(user.name, 'Another')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.username, 'anotheruser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_login_invalid(self):
        # Intento de inicio de sesión con credenciales inválidas
        login = self.client.login(username='testuser', password='wrongpassword')
        self.assertFalse(login)

    def test_login_valid(self):
        # Intento de inicio de sesión con credenciales válidas
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)
        
        # Verificar que el usuario esté autenticado
        response = self.client.get(reverse('home_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenido')

    def test_create_user_with_existing_username(self):
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)

#requerimiento 1.2
class UserRegistrationTest(TestCase):

    def setUp(self):
        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        # Crear un usuario no administrador
        self.regular_user = User.objects.create_user(
            username='regularuser',
            name='Regular',
            last_name='User',
            password='regularpassword',
            is_admin=False
        )

    def test_admin_can_register_user(self):
        self.client.login(username='adminuser', password='adminpassword')
        
        form_data = {
            'username': 'newuser',
            'name': 'New',
            'last_name': 'User',
            'password': 'newpassword',
            'password2': 'newpassword',
            'is_admin': False
        }
        
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertEqual(user.username, 'newuser')

#     def test_clean_username_unique(self):
#         form_data = {
#             'username': 'regularuser',
#             'name': 'New',
#             'last_name': 'User',
#             'password': 'newpassword',
#             'password2': 'newpassword',
#             'is_admin': False
#         }
        
#         form = UserRegisterForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('Este nombre de usuario ya está en uso. Elige otro.', form.errors['username'])

#     def test_clean_password_length(self):
#         form_data = {
#             'username': 'newuser',
#             'name': 'New',
#             'last_name': 'User',
#             'password': 'short',
#             'password2': 'short',
#             'is_admin': False
#         }
        
#         form = UserRegisterForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('La contraseña debe tener más de 5 caracteres.', form.errors['password'])

#     def test_clean_password_match(self):
#         form_data = {
#             'username': 'newuser',
#             'name': 'New',
#             'last_name': 'User',
#             'password': 'password1',
#             'password2': 'password2',
#             'is_admin': False
#         }
        
#         form = UserRegisterForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('Las contraseñas no coinciden.', form.errors['password2'])

#     def test_clean_name_valid(self):
#         form_data = {
#             'username': 'newuser',
#             'name': 'New123',
#             'last_name': 'User',
#             'password': 'newpassword',
#             'password2': 'newpassword',
#             'is_admin': False
#         }
        
#         form = UserRegisterForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('El nombre solo puede contener letras.', form.errors['name'])

#     def test_clean_last_name_valid(self):
#         form_data = {
#             'username': 'newuser',
#             'name': 'New',
#             'last_name': 'User123',
#             'password': 'newpassword',
#             'password2': 'newpassword',
#             'is_admin': False
#         }
        
#         form = UserRegisterForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('El apellido solo puede contener letras.', form.errors['last_name'])

# #requerimiento 1.3
# class UserUpdateFormTest(TestCase):
    def setUp(self):
        # Crear un usuario administrador
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        # Crear un usuario no administrador
        self.regular_user = User.objects.create_user(
            username='regularuser',
            name='Regular',
            last_name='User',
            password='regularpassword',
            is_admin=False
        )

    def test_admin_can_update_user(self):
        self.client.login(username='adminuser', password='adminpassword')
        
        # Datos para actualizar el usuario regular_user
        form_data = {
            'username': 'regularuser',
            'name': 'Updated Regular',
            'last_name': 'User Updated',
            'is_admin': True  # Cambiar el estado de administrador
        }
        
        # Obtener el usuario a través de su id
        user_to_update = User.objects.get(username='regularuser')
        
        # Crear una instancia del formulario de actualización con los datos
        form = UserUpdateForm(data=form_data, instance=user_to_update)
        
        # Verificar que el formulario sea válido
        self.assertTrue(form.is_valid())
        
        # Guardar los cambios en el usuario
        updated_user = form.save()
        
        # Verificar que los datos se han actualizado correctamente
        self.assertEqual(updated_user.name, 'Updated Regular')
        self.assertEqual(updated_user.last_name, 'User Updated')
        self.assertTrue(updated_user.is_admin)  # Verificar que el usuario ahora es administrador