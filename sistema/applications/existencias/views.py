# Fecha de Creación: 14/04/2024
# Autor: Vivian Carolina Hincapie Escobar 
# Última modificación: 01/06/2024

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.users.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse_lazy
from applications.materiaprima.models import MateriaPrimaGenerica
from applications.insumos.models import InsumosGenerico
from applications.productoterminado.models import ProductoTerminadoGenerico

class ExistenciasMateriaPrimaListView(LoginRequiredMixin, ListView):
    '''Clase encargada de la vista que muestra las existencias de Materia Prima'''
    model = MateriaPrimaGenerica
    template_name = "existencias/stock_mp.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by = 10
    context_object_name = "stock_mp"

    def get_queryset(self):
        '''Funcion que recibe la palabra clave en la barra de busqueda y filtra el resultado'''
        palabra_clave = self.request.GET.get("kword", '')
        tipo_materia_prima = self.request.GET.get('tipo', None)
        
        queryset = MateriaPrimaGenerica.objects.all()

        if palabra_clave:
            queryset = queryset.filter(mp_nombre__icontains=palabra_clave)
        
        if tipo_materia_prima and tipo_materia_prima != 'Todos':
            queryset = queryset.filter(mp_tipo=tipo_materia_prima)

        queryset = queryset.order_by(F('cantidad_total').desc())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['tipo_materia_prima'] = self.request.GET.get('tipo', 'Todos')
        context['palabra_clave'] = self.request.GET.get('kword', '')

        return context
        
class ExistenciasInsumosListView(LoginRequiredMixin, ListView):
    '''Clase encargada de la vista que muestra las existencias de Insumos'''
    model=InsumosGenerico
    template_name = "existencias/stock_insumos.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by= 10
    context_object_name = "stock_it"

class ExistenciasProductoTerminadoListView(LoginRequiredMixin, ListView):
    '''Clase encargada de la vista que muestra las existencias de Producto Terminado'''
    model = ProductoTerminadoGenerico
    template_name = "existencias/stock_pt.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by = 10
    context_object_name = "stock_pt"

    def get_queryset(self):
        '''Funcion que recibe la palabra clave en la barra de busqueda y filtra el resultado'''

        palabra_clave = self.request.GET.get("kword", '')
        
        queryset = ProductoTerminadoGenerico.objects.all()

        if palabra_clave:
            queryset = queryset.filter(pt_nombre__icontains=palabra_clave)
        queryset = queryset.order_by(F('cantidad_total').desc())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palabra_clave'] = self.request.GET.get('kword', '')
        return context

@login_required
#Autor: Vivian carolina Hincapie Escobar
def registrar_salida(request):
    '''
    Vista para registrar las salidas de producto terminado 
    '''
    producto = ProductoTerminadoGenerico.objects.all()

    if request.method == 'POST':
      
        return redirect(reverse_lazy('existencias_app:stock_pt'))
    
    return render(request, 'existencias/registrar_salida.html',{'producto': producto})