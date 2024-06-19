from django.test import TestCase
from applications.users.models import User
from .models import Proveedores
from .forms import ProveedorCreateForm,ProveedoresUpdateForm

class ProveedoresTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        # Crear un proveedor de prueba
        self.proveedor = Proveedores.objects.create(
            nit=1234567890,
            prov_nombre='Proveedor Test',
            prov_telefono='1234567890'
        )

    def test_proveedor_model(self):
        proveedor = Proveedores.objects.get(nit=1234567890)
        self.assertEqual(proveedor.prov_nombre, 'Proveedor Test')
        self.assertEqual(proveedor.prov_telefono, '1234567890')

    def test_proveedor_create_form_valid(self):
        form_data = {
            'nit': 9876543210,
            'prov_nombre': 'Nuevo Proveedor',
            'prov_telefono': '9876543210'
        }
        form = ProveedorCreateForm(data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_proveedor_create_form_invalid(self):
        form_data = {
            'nit': 9876543210,
            'prov_nombre': 'Nuevo Proveedor',
            'prov_telefono': '12345'  # Teléfono con menos de 10 dígitos
        }
        form = ProveedorCreateForm(data=form_data)
        form.is_valid()
        self.assertFalse(form.is_valid())

    def test_proveedores_update_form_valid(self):
        form_data = {
            'nit': 1234567890,
            'prov_nombre': 'Proveedor Actualizado',
            'prov_telefono': '1234567890'
        }
        form = ProveedoresUpdateForm(instance=self.proveedor, data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_proveedores_update_form_invalid(self):
        form_data = {
            'nit': 1234567890,
            'prov_nombre': 'Proveedor Actualizado',
            'prov_telefono': '12345'  # Teléfono con menos de 10 dígitos
        }
        form = ProveedoresUpdateForm(instance=self.proveedor, data=form_data)
        form.is_valid()
        self.assertFalse(form.is_valid())