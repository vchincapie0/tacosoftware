from django.urls import path
from . import views

app_name='pedidos_app'

urlpatterns = [
    path('list_pedidos/',views.PedidosListView.as_view(),name='list_pedidos'),
    path('pedidos/export/xls', views.export_pedidos_to_excel, name='export_pedidos_excel'),
    path('pedidos/export/csv', views.export_pedidos_to_csv, name='export_pedidos_csv'),
    path('add_pedidos/',views.PedidosCreateView.as_view(),name='add_pedidos'),
    path('add_mp_pedidos/',views.PedidosAddMpCreateView.as_view(),name='add__mp_pedidos'),
    path('add_it_pedidos/',views.PedidosAddInsumosCreateView.as_view(),name='add__it_pedidos'),
    path('add_prov_pedidos/',views.PedidosAddProveedoresCreateView.as_view(),name='add__prov_pedidos'),
    path('update_pedidos/<pk>',views.PedidosUpdateView.as_view(),name='update_pedidos'),
    path('delete_pedidos/<pk>',views.PedidosDeleteView.as_view(),name='delete_pedidos'),
    path('pedidos_audit/',views.PedidosAuditListView.as_view(),name='pedidos_audit'),


    
    





]