from django.urls import path
from . import views

app_name='procesamientos_app'

urlpatterns = [
    path('procesamientos/',views.ProcesamientosView.as_view(),name='procesamientos'),
    path('select_coccion/',views.select_coccion_view,name='select_coccion'),
    path('select_picado/',views.select_picado_view, name='select_picado'),
    path('procesamiento_coccion/<int:producto_id>/',views.ingresar_peso_materias_primas_coccion,name='procesamiento_coccion'),
    path('procesamiento_picado/<int:producto_id>/',views.ingresar_peso_materias_primas_picado,name='procesamiento_picado'),
    path('caracteristicas_organolepticas/<str:lote>',views.caracteristicas_organolepticas_pt, name='caracteristicas_organolepticas'),
    path('ingresar_empaques/',views.empaque_vacio, name='empaques'),
    path('equipos/',views.EquiposListView.as_view(),name='equipos'),
    path('add_equipos/',views.EquiposcreateView.as_view(),name='add_equipos'),
    path('delete_equipo/<pk>',views.EquiposDeleteView.as_view(),name='delete_equipo'),
    path('edit_equipo/<pk>',views.EquiposUpdateView.as_view(),name='edit_equipo'),
    
]