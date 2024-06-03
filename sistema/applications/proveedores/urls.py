# Fecha de Creación: 16/02/2024
# Autor: Vivian Carolina Hincapie Escobar
# Última modificación: 16/05/2024

from django.urls import path
from applications.users.decorators import admin_required
from . import views

app_name='proveedores_app'

urlpatterns = [
    path('list_proveedores/',admin_required(views.ProveedoresListView.as_view()),name='list_proveedores'),
    path('proveedores/export/xls',admin_required(views.export_proveedores_to_excel), name='export_proveedores_excel'),
    path('proveedores/export/csv',admin_required(views.export_proveedores_to_csv), name='export_proveedores_cvs'),
    path('add_proveedor/',admin_required(views.ProveedoresCreateView.as_view()),name='add_proveedores'),
    path('edit_proveedor/<pk>',admin_required(views.ProveedorUpdateView.as_view()),name='update_proveedores'),
    path('delete_proveedor/<pk>',admin_required(views.ProveedoresDeleteView.as_view()),name='delete_proveedores'),
    path('proveedor_audit/',admin_required(views.ProveedoresAuditListView.as_view()),name='proveedor_audit'),

]