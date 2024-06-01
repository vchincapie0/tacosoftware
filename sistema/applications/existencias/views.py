from django.shortcuts import render
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from applications.materiaprima.models import MateriaPrimaGenerica
from applications.insumos.models import InsumosGenerico
from applications.productoterminado.models import ProductoTerminadoGenerico

class ExistenciasMateriaPrimaListView(LoginRequiredMixin, ListView):
    model = MateriaPrimaGenerica
    template_name = "existencias/stock_mp.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by = 10
    context_object_name = "stock_mp"

    def get_queryset(self):
        '''Function that retrieves the keyword from the search bar to filter results'''
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
        
        # Pass the type and keyword to the template to retain the state of the search and filter form
        context['tipo_materia_prima'] = self.request.GET.get('tipo', 'Todos')
        context['palabra_clave'] = self.request.GET.get('kword', '')

        return context
        
class ExistenciasInsumosListView(LoginRequiredMixin, ListView):
    model=InsumosGenerico
    template_name = "existencias/stock_insumos.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by= 10
    context_object_name = "stock_it"

class ExistenciasProductoTerminadoListView(LoginRequiredMixin, ListView):
    model = ProductoTerminadoGenerico
    template_name = "existencias/stock_pt.html"
    login_url = reverse_lazy('users_app:login')
    paginate_by = 10
    context_object_name = "stock_pt"

    def get_queryset(self):
        '''Function that retrieves the keyword from the search bar to filter results'''
        palabra_clave = self.request.GET.get("kword", '')
        
        queryset = ProductoTerminadoGenerico.objects.all()

        if palabra_clave:
            queryset = queryset.filter(mp_nombre__icontains=palabra_clave)
        queryset = queryset.order_by(F('cantidad_total').desc())

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palabra_clave'] = self.request.GET.get('kword', '')
        return context