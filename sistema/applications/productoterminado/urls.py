from django.urls import path
from applications.users.decorators import admin_required
from . import views

app_name='produ_app'

urlpatterns = [
    path('list_produ/',views.ProduListView.as_view(),name='list_produ'),
    path('update_produ/<pk>',views.ProduUpdateView.as_view(),name='update_produ'),
    path('updatecaracteristicas_pt/<pk>',views.CaracteristicasProductoTerminadoUpdateView.as_view(),name='updatecaracteristicas_pt'),
    path('detail_PT/<str:pt_lote>',views.ProductoTerminadoDetailView.as_view(),name='detail_PT'),
    path('empaque_update/<pk>',views.EmpaqueProductoTerminadoUpdateView.as_view(),name='empaque_update'),
    path('vacio_update/<pk>',views.VacioProductoTerminadoUpdateView.as_view(),name='vacio_update'),
    path('list_pt_generico/',admin_required(views.ProductoTerminadoGenericoListView.as_view()),name='list_pt_generico'),
    path('add_pt_generico/',admin_required(views.ProductoTerminadoGenericoCreateView.as_view()),name='add_pt_generico'),
    path('update_pt_generico/<pk>',admin_required(views.ProductoTerminadoGenericoUpdateView.as_view()),name='update_pt_generico'),
    path('delete_pt_generico/<pk>',admin_required(views.ProductoTerminadoGenericoDeleteView.as_view()),name='delete_pt_generico'),
    path('producto_audit/',admin_required(views.ProductoAuditListView.as_view()),name='producto_audit'),
    path('productoterminado/export/xls',admin_required(views.export_productoterminado_to_excel), name='export_productoterminado_excel'),
    path('productoterminado/export/cvs',admin_required(views.export_productoterminado_to_csv), name='export_productoterminado_cvs'),











]