from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView,CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
#Importacion de modelos y formularios
from applications.materiaprima.models import MateriaPrimaGenerica
from applications.productoterminado.models import (
    ProductoTerminadoGenerico, 
    ProductoTerminado,
    CaracteristicasOrganolepticasPT,
)
from .models import Picado,PicadoMateriaPrima,Coccion,Equipos
from .forms import PicadoForm,addEquipos,EquiposUpdateForm

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
        return redirect(reverse_lazy('procesamientos_app:procesamiento_coccion', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    else:
        return render(request, 'procesamientos/coccion/select_coccion.html', {'productos': productos})

def select_picado_view(request):
    '''Vista para seleccionar que producto de picado se va a realizar'''
    productos = ProductoTerminadoGenerico.objects.filter(pt_tipo='1')
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect(reverse_lazy('procesamientos_app:procesamiento_picado', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    return render(request, 'procesamientos/picado/select_picado.html', {'productos': productos})

def ingresar_peso_materias_primas_coccion(request, producto_id):
    producto = get_object_or_404(ProductoTerminadoGenerico, pk=producto_id)
    materias_primas = producto.materiaPrimaUsada.all()

    if request.method == 'POST':
        # Procesar los datos del primer fieldset
        for materia_prima in materias_primas:
            peso = int(request.POST.get(f"peso_{materia_prima.id}"))
            if peso > materia_prima.cantidad_total:
                # Redirigir de vuelta al formulario con un mensaje de error
                return render(request, 'procesamientos/coccion/ingreso_peso_mp.html', {
                    'producto': producto,
                    'materias_primas': materias_primas,
                    'error': f'El peso ingresado para {materia_prima.mp_nombre} excede la cantidad disponible.'
                })
        
        # Procesar los datos del segundo y tercer fieldset
        peso_post_produccion = request.POST.get("peso_post_produccion")
        tiempo_coccion = request.POST.get("tiempo_coccion")
        temperatura = request.POST.get("temperatura")
        olor = request.POST.get("check_olor") == 'on'
        sabor = request.POST.get("check_sabor") == 'on'
        color = request.POST.get("check_color") == 'on'
        textura = request.POST.get("check_textura") == 'on'
        observaciones = request.POST.get("observacion")

        # Guardar los datos en CaracteristicasOrganolepticasPT
        caracteristicas = CaracteristicasOrganolepticasPT(
            producto=producto,
            observaciones=observaciones,
            olor=olor,
            sabor=sabor,
            color=color,
            textura=textura
        )
        caracteristicas.save()

        # Guardar los datos en Picado
        picado = Picado(
            pica_pesoMPposproceso=peso_post_produccion,
            pica_check='0'  # Default to 'Aprobado' for now
        )
        picado.save()
        picado.pica_producto.add(producto)
        picado.save()

        # Redirigir a una página de éxito
        return redirect(reverse_lazy('procesamientos_app:empaques'))
    return render(request, 'procesamientos/coccion/ingreso_peso_mp.html', {'producto': producto, 'materias_primas': materias_primas})

def ingresar_peso_materias_primas_picado(request, producto_id):
    producto = get_object_or_404(ProductoTerminadoGenerico, id=producto_id)
    materias_primas = producto.materiaPrimaUsada.all()
    
    if request.method == 'POST':
        picado_form = PicadoForm(request.POST)
        if picado_form.is_valid():
            pica_pesoPostProcesamiento=picado_form.cleaned_data['pica_pesoPostProcesamiento']
            pica_merma=picado_form.cleaned_data['pica_merma']
            pica_check = picado_form.cleaned_data['pica_check']
            print(f'peso post: {pica_pesoPostProcesamiento} - merma: {pica_merma}- check: {pica_check}')
            picado = picado_form.save(commit=False)
            
            # Crear ProductoTerminado con pt_cantidad inicializado a 0
            producto_terminado = ProductoTerminado.objects.create(
                pt_cantidad=0,
                pt_nombre=producto,
                pt_fechapreparacion=timezone.now(),
                pt_fechavencimiento=timezone.now() + timezone.timedelta(days=30)
            )
            
            picado.save()
            picado.pica_producto.add(producto_terminado)
            picado.save()

            # Guardar la cantidad de cada materia prima utilizada
            for materia_prima in materias_primas:
                peso = int(request.POST.get(f'peso_{materia_prima.id}', 0))
                if peso > 0:
                    PicadoMateriaPrima.objects.create(
                        picado=picado,
                        materia_prima=materia_prima,
                        cantidad=peso
                    )
                    # Restar la cantidad de materia prima utilizada
                    materia_prima.cantidad_total -= peso
                    materia_prima.save()

            return redirect(reverse_lazy('procesamientos_app:empaques'))

    else:
        picado_form = PicadoForm()

    return render(request, 'procesamientos/picado/ingreso_peso_mp.html', {'producto': producto, 'materias_primas': materias_primas})

def caracteristicas_organolepticas_pt(request):
    
    return render(request, 'procesamientos/caracteristicasorganolepticasPt.html')

def empaque_vacio(request):
    
    return render(request, 'procesamientos/empaque.html')

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



