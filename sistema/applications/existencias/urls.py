from django.urls import path
from . import views 

app_name='existencias_app'

urlpatterns = [
    path('existencias_mp/',views.ExistenciasMateriaPrimaListView.as_view(),name='stock_mp'),
    path('existencias_it/',views.ExistenciasInsumosListView.as_view(),name='stock_it'),
    path('existencias_pt/',views.ExistenciasProductoTerminadoListView.as_view(),name='stock_pt'),

]