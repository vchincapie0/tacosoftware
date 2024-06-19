import unittest
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from applications.users.models import User
from .models import Pedidos
from .forms import PedidosCreateForm, PedidosUpdateForm, PedidosAddInsumosCreateFrom, PedidosAddMpCreateFrom, PedidosAddProveedorCreateFrom

class TestPedidosForms(TestCase):

    def setUp(self):
         # Crear un usuario para las pruebas
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        pass

    def test_pedi_fecha_validation(self):
        self.client.login(username='adminuser', password='adminpassword')

        form_data = {
            'ref_pedido': 1,
            'pedi_fecha': date.today() - timedelta(days=2),  # Fecha dos días atrás
            'pedi_estado': '0',
            'pedi_comprobatePago': '123ABC',
            'pedi_proveedor': 1,
            'pedi_materiaprima': [],
            'pedi_insumos': [],
        }
        form = PedidosCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('pedi_fecha', form.errors)
        
    def test_ref_pedido_unique_validation(self):
        # Simular un pedido existente con la misma referencia
        Pedidos.objects.create(ref_pedido=1, pedi_fecha=timezone.now().date(), pedi_estado='0',
                               pedi_comprobatePago='123ABC', pedi_proveedor_id=1)
        
        form_data = {
            'ref_pedido': 1,
            'pedi_fecha': timezone.now().date(),
            'pedi_estado': '0',
            'pedi_comprobatePago': '123ABC',
            'pedi_proveedor': 1,
            'pedi_materiaprima': [],
            'pedi_insumos': [],
        }
        form = PedidosCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ref_pedido', form.errors)

if __name__ == '__main__':
    unittest.main()

class TestPedidosAddForms(TestCase):

    def setUp(self):
         # Crear un usuario para las pruebas
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        pass

    def test_mp_cantidad_validation(self):

        self.client.login(username='adminuser', password='adminpassword')

        form_data = {
            'mp_lote': 1,
            'mp_nombre': 1,
            'mp_cantidad': -5,  # Cantidad negativa
            'mp_fechallegada': date.today(),
            'mp_fechavencimiento': date.today() + timedelta(days=5),
        }
        form = PedidosAddMpCreateFrom(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mp_cantidad', form.errors)
        
    def test_it_cantidad_validation(self):
        form_data = {
            'it_codigo': 1,
            'it_nombre': 1,
            'it_cantidad': 0,  # Cantidad no positiva
            'it_fechaEntrega': date.today(),
            'it_estado': '0',
        }
        form = PedidosAddInsumosCreateFrom(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('it_cantidad', form.errors)

if __name__ == '__main__':
    unittest.main()

class TestPedidosUpdate(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas
        self.admin_user = User.objects.create_user(
            username='adminuser',
            name='Admin',
            last_name='User',
            password='adminpassword',
            is_admin=True
        )

        # Crear un pedido de ejemplo
        self.pedido = Pedidos.objects.create(
            ref_pedido=1,
            pedi_user=self.user,
            pedi_fecha=timezone.now().date(),
            pedi_estado='0',
            pedi_comprobatePago='123ABC',
            pedi_proveedor_id=1
        )

    def test_pedido_modification(self):
        # Autenticar al usuario
        self.client.login(username='adminuser', password='adminpassword')

        # Datos para modificar el pedido
        updated_data = {
            'ref_pedido': 1,
            'pedi_user': self.user.id,
            'pedi_fecha': timezone.now().date(),
            'pedi_estado': '1',  # Cambiar el estado
            'pedi_comprobatePago': '456DEF',  # Cambiar el comprobante de pago
            'pedi_proveedor': 1,
            'pedi_materiaprima': [],
            'pedi_insumos': [],
        }

        # Crear el formulario de actualización con los datos modificados
        form = PedidosUpdateForm(instance=self.pedido, data=updated_data)
        self.assertTrue(form.is_valid(), form.errors)

        # Guardar los cambios en el pedido
        updated_pedido = form.save()

        # Verificar que los campos se hayan actualizado correctamente
        self.assertEqual(updated_pedido.pedi_estado, '1')
        self.assertEqual(updated_pedido.pedi_comprobatePago, '456DEF')

class TestPedidosAddProveedorForm(TestCase):

    def test_prov_telefono_validation(self):
        form_data = {
            'nit': 123,
            'prov_nombre': 'Proveedor 1',
            'prov_telefono': '12345',  # Teléfono con menos de 10 dígitos
        }
        form = PedidosAddProveedorCreateFrom(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prov_telefono', form.errors)
        
    def test_prov_nombre_validation(self):
        form_data = {
            'nit': 123,
            'prov_nombre': 'Proveedor 1 2',  # Nombre con números
            'prov_telefono': '1234567890',
        }
        form = PedidosAddProveedorCreateFrom(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prov_nombre', form.errors)

if __name__ == '__main__':
    unittest.main()
