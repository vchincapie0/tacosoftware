from django.urls import path
from applications.users.decorators import admin_required
from . import views

app_name='insumos_app'

urlpatterns = [
    path('list_insumos_generico/',admin_required(views.InsumosGenericoListView.as_view()),name='list_insumos_generico'),
    path('add_insumos_generico/',admin_required(views.InsumosGenericoCreateView.as_view()),name='add_insumos_generico'),
    path('update_insumos_generico/<pk>',admin_required(views.InsumosGenericoUpdateView.as_view()),name='update_insumos_generico'),
    path('delete_insumos_generico/<pk>',admin_required(views.InsumosGenericoDeleteView.as_view()),name='delete_insumos_generico'),
    path('list_insumos/',views.InsumosListView.as_view(),name='list_insumos'),
    path('update_insumos/<pk>',views.InsumosUpdateView.as_view(),name='update_insumos'),
    path('insumos_audit/',admin_required(views.InsumosAuditListView.as_view()),name='insumos_audit'),
    path('insumos/export/xls',admin_required(views.export_insumos_to_excel), name='export_insumos_excel'),
    path('insumos/export/cvs',admin_required(views.export_insumos_to_csv), name='export_insumos_cvs'),
]