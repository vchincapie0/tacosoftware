# Fecha de Creación: 04/03/2024
# Última modificación: 22/05/2024

from django.urls import path
from applications.users.decorators import admin_required
from . import views

app_name='facturas_app'

urlpatterns = [
    path('list_facturas/', views.FacturasListView.as_view(), name='list_factura'),
    path('facturas/export/xls', views.export_facturas_to_excel, name='export_facturas_excel'),
    path('facturas/export/cvs', views.export_facturas_to_csv, name='export_facturas_csv'),
    path('add_facturas/', views.FacturasCreateView.as_view(), name='add_factura'),
    path('edit_facturas/<pk>', views.FacturasUpdateView.as_view(), name='edit_factura'),
    path('delete_facturas/<pk>', views.FacturasDeleteView.as_view(), name='delete_factura'),
    path('list_IVA/',admin_required(views.IVAListView.as_view()), name='list_IVA'),
    path('add_IVA/',admin_required(views.IVACreateView.as_view()), name='add_IVA'),
    path('update_IVA/<pk>',admin_required(views.IVAUpdateView.as_view()), name='update_IVA'),
    path('delete_IVA/<pk>',admin_required(views.IVADeleteView.as_view()), name='delete_IVA'),
    path('facturas_audit/', views.FacturasAuditListView.as_view(), name='factura_audit'),
]