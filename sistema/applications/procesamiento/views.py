from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView,CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
#Importacion de modelos y formularios
from applications.productoterminado.models import ProductoTerminadoGenerico
from .models import Picado,Coccion,Equipos
from .forms import addEquipos,EquiposUpdateForm

# Create your views here.

class ProcesamientosView(LoginRequiredMixin, TemplateView):
    '''Clase para mostrar los datos de Procesamiento'''
    template_name = "Procesamientos/procesamiento_view.html"
    login_url=reverse_lazy('users_app:login')

def select_coccion_view(request):
    '''Vista para seleccionar que producto de coccion se va a realizar'''
    productos = ProductoTerminadoGenerico.objects.filter(pt_tipo='0')
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect(reverse_lazy('procesamientos_app:ingresar_peso_materias_primas', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    else:
        return render(request, 'procesamientos/coccion/select_coccion.html', {'productos': productos})

def select_picado_view(request):
    '''Vista para seleccionar que producto de picado se va a realizar'''
    productos = ProductoTerminadoGenerico.objects.filter(pt_tipo='1')
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect(reverse_lazy('procesamientos_app:ingresar_peso_materias_primas', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    return render(request, 'procesamientos/picado/select_picado.html', {'productos': productos})

def ingresar_peso_materias_primas(request, producto_id):
    producto = ProductoTerminadoGenerico.objects.get(pk=producto_id)
    materias_primas = producto.materiaPrimaUsada.all()
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect('ruta_de_exito')
    else:
        return render(request, 'procesamientos/ingreso_peso_mp.html', {'producto': producto, 'materias_primas': materias_primas})


class CoccionListView(LoginRequiredMixin, ListView):
    '''Clase para mostrar los datos de picado'''
    model = Coccion
    template_name = "Procesamientos/coccion.html"
    login_url=reverse_lazy('users_app:login')
    paginate_by=10
    context_object_name = 'procesamientos'

    def get_queryset(self):
            '''Funcion que toma de la barra de busqueda la pablabra clave para filtrar datos borrados'''
            lista = Coccion.objects.filter(
            )
            return lista

class EquiposListView(LoginRequiredMixin, ListView):
    '''Clase para mostrar los datos de equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/equipos.html"
    login_url=reverse_lazy('users_app:login')
    paginate_by=10
    context_object_name = 'procesamientos'

    def get_queryset(self):
            '''Funcion que toma de la barra de busqueda la pablabra clave para filtrar datos borrados'''
            lista = Equipos.objects.filter(
                deleted=False  # Solo picados activos
            )
            return lista


class EquiposcreateView(LoginRequiredMixin,CreateView):
    '''Vista para crear  de equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/add_equipo.html"
    login_url=reverse_lazy('home_app:home')
    form_class=addEquipos
    success_url= reverse_lazy('procesamientos_app:equipos')

class EquiposUpdateView(LoginRequiredMixin, UpdateView):
    '''Vista para actualizar los datos de Equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/edit_equipo.html"
    login_url=reverse_lazy('users_app:login')
    form_class=EquiposUpdateForm
    success_url= reverse_lazy('procesamientos_app:equipos')

class EquiposDeleteView(LoginRequiredMixin,DeleteView):
    '''Vista para borrar equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/delete_equipo.html"
    login_url=reverse_lazy('users_app:login')
    success_url= reverse_lazy('procesamientos_app:equipos')



