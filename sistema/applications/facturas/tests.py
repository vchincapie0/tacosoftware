from django.test import TestCase
from datetime import datetime, timedelta
from .models import Facturas, IVA, FacturasAudit
from .forms import FacturaCreateForm, FacturaUpdateForm, FacturasAuditFilterForm
from applications.proveedores.models import Proveedores
from applications.pedidos.models import Pedidos
from applications.users.models import User

class FacturasTestCase(TestCase):
    def setUp(self):
        # Crear instancias de prueba necesarias
        self.iva = IVA.objects.create(valor=0.19)  # Ejemplo de un objeto IVA
        self.proveedor = Proveedores.objects.create(nit=1234567890, prov_nombre='Proveedor Test', prov_telefono='1234567890')
        self.pedido = Pedidos.objects.create(numero_pedido='P001', fecha_pedido=datetime.now())
        
        # Crear una factura de prueba
        self.factura = Facturas.objects.create(
            num_factura=1,
            fac_numeroPedido=self.pedido,
            fac_numeroUnidades=10,
            fac_subtotal=100.0,
            fac_iva=self.iva,
            fac_total=119.0,
        )

    def test_factura_model(self):
        factura = Facturas.objects.get(num_factura=1)
        self.assertEqual(factura.fac_numeroUnidades, 10)
        self.assertEqual(factura.fac_subtotal, 100.0)
        self.assertEqual(factura.fac_total, 119.0)

    def test_factura_create_form_valid(self):
        form_data = {
            'num_factura': 2,
            'fac_numeroPedido': self.pedido.id,
            'fac_numeroUnidades': 5,
            'img_factura': None,
            'fac_subtotal': 50.0,
            'fac_iva': self.iva.id,
        }
        form = FacturaCreateForm(data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_factura_create_form_invalid(self):
        form_data = {
            'num_factura': 3,
            'fac_numeroPedido': self.pedido.id,
            'fac_numeroUnidades': -5,  # Número de unidades negativo
            'img_factura': None,
            'fac_subtotal': 50.0,
            'fac_iva': self.iva.id,
        }
        form = FacturaCreateForm(data=form_data)
        form.is_valid()
        self.assertFalse(form.is_valid())

    def test_factura_update_form_valid(self):
        form_data = {
            'num_factura': 1,  # Mismo número de factura para actualizar
            'fac_numeroPedido': self.pedido.id,
            'fac_numeroUnidades': 15,
            'img_factura': None,
            'fac_subtotal': 150.0,
            'fac_iva': self.iva.id,
        }
        form = FacturaUpdateForm(instance=self.factura, data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())

    def test_factura_update_form_invalid(self):
        form_data = {
            'num_factura': 1,
            'fac_numeroPedido': self.pedido.id,
            'fac_numeroUnidades': -5,  # Número de unidades negativo
            'img_factura': None,
            'fac_subtotal': 50.0,
            'fac_iva': self.iva.id,
        }
        form = FacturaUpdateForm(instance=self.factura, data=form_data)
        form.is_valid()
        self.assertFalse(form.is_valid())

    def test_facturas_audit_filter_form(self):
        form_data = {
            'factura': self.factura.num_factura,
            'action': 'C',
            'changed_by': None,
            'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
            'pedido': self.pedido.id,
            'proveedor': self.proveedor.id,
        }
        form = FacturasAuditFilterForm(data=form_data)
        form.is_valid()
        self.assertTrue(form.is_valid())
