from django.urls import path
from applications.users.decorators import admin_required
from . import views

app_name='mp_app'

urlpatterns = [
    path('mpgeneric_list/',admin_required(views.MateriaPrimaGenericaListView.as_view()),name='listaGenerica_mp'),
    path('add_mp_generica/',admin_required(views.MateriaPrimaGenericaCreateView.as_view()),name='add_mp_generica'),
    path('update_mp_generica/<pk>',admin_required(views.MateriaPrimaGenericaUpdateView.as_view()),name='update_mp_generica'),
    path('delete_mp_generica/<pk>',admin_required(views.MateriaPrimaGenericaDeleteView.as_view()),name='delete_mp_generica'),
    path('mp_list/',views.MateriaPrimaListView.as_view(),name='lista_mp'),
    path('mp_caracteristicas/',views.CaracteristicasMateriaPrimaCreateView.as_view(),name='caracteristicas_mp'),
    path('mp_update_caracteristicas/<pk>',views.CaracteristicasMateriaPrimaUpdateView.as_view(),name='updateCaracteristicas_mp'),
    path('desinfeccion_generico/',admin_required(views.DesinfectanteGenericoListView.as_view()),name='desinfeccion_generico'),
    path('add_desinfeccion_generico/',admin_required(views.DesinfectanteGenericoCreateView.as_view()),name='add_desinfeccion_generico'),
    path('update_desinfeccion_generico/<pk>',admin_required(views.DesinfectanteGenericoUpdateView.as_view()),name='update_desinfeccion_generico'),
    path('delete_desinfeccion_generico/<pk>',admin_required(views.DesinfectanteGenericoDeleteView.as_view()),name='delete_desinfeccion_generico'),
    path('mp_desinfeccion/',views.DesinfeccionMateriaPrimaCreateView.as_view(),name='desinfeccion_mp'),
    path('mp_update_desinfeccion/<pk>',views.DesinfeccionMateriaPrimaUpdateView.as_view(),name='updateDesinfeccion_mp'),
    path('mp_detail/<pk>',views.MateriaPrimaDetailView.as_view(),name='detail_mp'),
    path('mp_update/<pk>',views.MateriaPrimaUpdateView.as_view(),name='mp_update'),
    path('mp_audit/',admin_required(views.MateriaAuditListView.as_view()),name='mp_audit'),
    path('materiaprima/export/xls',admin_required(views.export_materiaprima_to_excel), name='export_materiaprima_excel'),
    path('materiaprima/export/cvs',admin_required(views.export_materiaprima_to_csv), name='export_materiaprima_cvs'),

]