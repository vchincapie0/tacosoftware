from django.urls import path
from . import views

app_name='procesamientos_app'

urlpatterns = [
    path('procesamientos/',views.ProcesamientosView.as_view(),name='procesamientos'),
    path('select_coccion/',views.select_coccion_view,name='select_coccion'),
    path('select_picado/',views.select_picado_view, name='select_picado'),
    path('ingresar_peso_mp/<int:producto_id>/',views.ingresar_peso_materias_primas,name='ingresar_peso_materias_primas'),
    path('coccion/',views.CoccionListView.as_view(),name='coccion'),
    path('equipos/',views.EquiposListView.as_view(),name='equipos'),
    path('add_equipos/',views.EquiposcreateView.as_view(),name='add_equipos'),
    path('delete_equipo/<pk>',views.EquiposDeleteView.as_view(),name='delete_equipo'),
    path('edit_equipo/<pk>',views.EquiposUpdateView.as_view(),name='edit_equipo'),
    
]