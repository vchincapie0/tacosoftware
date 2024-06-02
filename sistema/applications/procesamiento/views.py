#Importación de bibliotecas necesarias
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView,CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
#Importación de modelos y formularios
from applications.productoterminado.models import (
    ProductoTerminadoGenerico, 
    ProductoTerminado,
    EmpaqueProductoTerminado,
    Vacio,
)
from .models import (
    Picado,
    PicadoMateriaPrima,
    Coccion,
    CoccionMateriaPrima,
    Equipos)
from .forms import addEquipos,EquiposUpdateForm
from applications.productoterminado.forms import (CaracteristicasOrganolepticasPTForm)

#Autor: Daniel Castro Mercado
class ProcesamientosView(LoginRequiredMixin, TemplateView):
    '''Clase para mostrar los datos de Procesamiento'''
    template_name = "Procesamientos/procesamiento_view.html"
    login_url=reverse_lazy('users_app:login')

#Autor: Daniel Castro Mercado
def select_coccion_view(request):
    '''Vista para seleccionar que producto de coccion se va a realizar'''
    productos = ProductoTerminadoGenerico.objects.filter(pt_tipo='0')
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect(reverse_lazy('procesamientos_app:procesamiento_coccion', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    else:
        return render(request, 'procesamientos/coccion/select_coccion.html', {'productos': productos})

#Autor: Daniel Castro Mercado
def select_picado_view(request):
    '''Vista para seleccionar que producto de picado se va a realizar'''
    productos = ProductoTerminadoGenerico.objects.filter(pt_tipo='1')
    if request.method == 'POST':
        # Procesar los datos del formulario aquí
        # Redirigir a la página de éxito o a donde sea necesario
        return redirect(reverse_lazy('procesamientos_app:procesamiento_picado', kwargs={'producto_id': request.POST.get('producto_terminado')}))
    return render(request, 'procesamientos/picado/select_picado.html', {'productos': productos})

#Autor: Vivian carolina Hincapie Escobar
def ingresar_peso_materias_primas_coccion(request, producto_id):
    '''
    Vista para ingresar el peso de las materias primas para el proceso de cocción.
    Crea instancias de ProductoTerminado, Coccion, y CoccionMateriaPrima.
    Deduce la cantidad del inventario de materias primas.
    '''  
    producto = get_object_or_404(ProductoTerminadoGenerico, id=producto_id)
    materias_primas = producto.materiaPrimaUsada.all()
    
    if request.method == 'POST':
         # Crear la instancia de ProductoTerminado
        producto_terminado = ProductoTerminado(
            pt_cantidad=0,  # Cantidad inicial es 0
            pt_nombre=producto,
            pt_fechapreparacion=timezone.now(),
            pt_fechavencimiento=timezone.now() + timezone.timedelta(days=20)  # Ajusta esto según tus necesidades
        )
        producto_terminado.save()
        
        # Después de guardar la instancia de ProductoTerminado, obtén el número de lote
        lote = producto_terminado.pt_lote

        # Crear la instancia de Picado
        coccion = Coccion(
            cocc_producto=producto_terminado,
            cocc_cantidad_total=request.POST['cocc_cantidad_total'],
            cocc_pesoPostProcesamiento=request.POST['cocc_pesoPostProcesamiento'],
            cocc_merma=request.POST['cocc_merma'],
            cocc_tiempoCoccion=request.POST['cocc_tiempoCoccion'],
            cocc_temperaturafinal=request.POST['cocc_temperaturafinal'],
            cocc_check=request.POST['cocc_check']
        )
        coccion.save()
        
         # Guardar los pesos de materias primas
        for materia_prima in materias_primas:
            peso = request.POST.get(f'peso_{materia_prima.id}')
            if peso:
                peso = int(peso)  # Convertir el peso a entero
                print(f'Guardando {peso}g de {materia_prima.mp_nombre}')
                coccion_materia_prima = CoccionMateriaPrima(
                    coccion=coccion,
                    materia_prima=materia_prima,
                    cantidad=peso
                )
                coccion_materia_prima.save()

                # Deducir la cantidad del inventario
                materia_prima.cantidad_total -= peso
                materia_prima.save()
        return redirect(reverse_lazy('procesamientos_app:caracteristicas_organolepticas', kwargs={'lote': lote}))
    return render(request, 'procesamientos/coccion/ingreso_peso_mp.html', {'producto': producto, 'materias_primas': materias_primas})
 
#Autor: Vivian carolina Hincapie Escobar       
def ingresar_peso_materias_primas_picado(request, producto_id):
    '''
    Vista para ingresar el peso de las materias primas para el proceso de picado.
    Crea instancias de ProductoTerminado, Picado, y PicadoMateriaPrima.
    Deduce la cantidad del inventario de materias primas.
    '''
    producto = get_object_or_404(ProductoTerminadoGenerico, id=producto_id)
    materias_primas = producto.materiaPrimaUsada.all()
    
    if request.method == 'POST':
         # Crear la instancia de ProductoTerminado
        producto_terminado = ProductoTerminado(
            pt_cantidad=0,  # Cantidad inicial es 0
            pt_nombre=producto,
            pt_fechapreparacion=timezone.now(),
            pt_fechavencimiento=timezone.now() + timezone.timedelta(days=20)  # Ajusta esto según tus necesidades
        )
        producto_terminado.save()
        
        # Después de guardar la instancia de ProductoTerminado, obtén el número de lote
        lote = producto_terminado.pt_lote

        # Crear la instancia de Picado
        picado = Picado(
            pica_producto=producto_terminado,
            pica_cantidad_total=request.POST['pica_cantidad_total'],
            pica_pesoPostProcesamiento=request.POST['pica_pesoPostProcesamiento'],
            pica_merma=request.POST['pica_merma'],
            pica_check=request.POST['pica_check']
        )
        picado.save()
        
         # Guardar los pesos de materias primas
        for materia_prima in materias_primas:
            peso = request.POST.get(f'peso_{materia_prima.id}')
            if peso:
                peso = int(peso)  # Convertir el peso a entero
                picado_materia_prima = PicadoMateriaPrima(
                    picado=picado,
                    materia_prima=materia_prima,
                    cantidad=peso
                )
                picado_materia_prima.save()

                # Deducir la cantidad del inventario
                materia_prima.cantidad_total -= peso
                materia_prima.save()

        return redirect(reverse_lazy('procesamientos_app:caracteristicas_organolepticas', kwargs={'lote': lote}))

    return render(request, 'procesamientos/picado/ingreso_peso_mp.html', {'producto': producto, 'materias_primas': materias_primas})

#Autor: Vivian carolina Hincapie Escobar
def caracteristicas_organolepticas_pt(request, lote):
    '''Vista para ingresar las características organolépticas de un producto terminado'''
    # Obtener el objeto ProductoTerminado asociado al número de lote
    producto = get_object_or_404(ProductoTerminado, pt_lote=lote)

    if request.method == 'POST':
        # Procesar el envío del formulario
        caracteristicas_form = CaracteristicasOrganolepticasPTForm(request.POST)
        if caracteristicas_form.is_valid():
            # Crear y guardar una instancia de CaracteristicasOrganolepticasPT
            caracteristicas = caracteristicas_form.save(commit=False)
            caracteristicas.producto = producto
            # Verificar si se han ingresado todas las características
            if (caracteristicas.olor and caracteristicas.sabor and
                    caracteristicas.color and caracteristicas.textura):
                caracteristicas.estado = '0'  # Estado exitoso
            else:
                caracteristicas.estado = '1'  # Estado incompleto
                caracteristicas.save()
                return redirect(reverse_lazy('produ_app:list_produ'))  # Redirigir a la lista de productos si falta alguna característica
            
            caracteristicas.save()
            return redirect(reverse_lazy('procesamientos_app:empaques', kwargs={'lote': lote}))  # Redirigir a la vista de empaques
    else:
        # Renderizar un formulario vacío para las solicitudes GET
        caracteristicas_form = CaracteristicasOrganolepticasPTForm()

    return render(request, 'procesamientos/caracteristicasorganolepticasPt.html', {'producto': producto, 'form': caracteristicas_form})

#Autor: Vivian carolina Hincapie Escobar
def empaque_vacio(request, lote):
    '''Vista para ingresar información sobre el empaque y el vacío de un producto terminado'''
    # Obtener el objeto ProductoTerminado asociado al número de lote
    producto = get_object_or_404(ProductoTerminado, pt_lote=lote)

    if request.method == 'POST':
        # Procesar los datos del formulario
        # Crear una instancia de EmpaqueProductoTerminado
        empaque = EmpaqueProductoTerminado(
            pt_lote=producto,
            emp_pesoKg = request.POST['peso_empaque'],
            emp_cantidadBolsas = request.POST['cantidad_empaque']
        )
        empaque.save()

        # Crear una instancia de Vacio
        vacio= Vacio(
           pt_lote=producto,
           cantidad_bolsas_rechazadas= request.POST['bolsas_rechazadas'],
           cantidad_bolsas_liberadas= request.POST['bolsas_liberadas'],
        )
        vacio.save()
        
        return redirect(reverse_lazy('produ_app:list_produ'))  # Redirigir a la lista de productos
    
    return render(request, 'procesamientos/empaque.html',{'producto': producto})  # Renderizar el formulario de empaque y vacío

#Autor: Daniel Castro Mercado
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

#Autor: Daniel Castro Mercado
class EquiposcreateView(LoginRequiredMixin,CreateView):
    '''Vista para crear  de equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/add_equipo.html"
    login_url=reverse_lazy('home_app:home')
    form_class=addEquipos
    success_url= reverse_lazy('procesamientos_app:equipos')

#Autor: Daniel Castro Mercado
class EquiposUpdateView(LoginRequiredMixin, UpdateView):
    '''Vista para actualizar los datos de Equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/edit_equipo.html"
    login_url=reverse_lazy('users_app:login')
    form_class=EquiposUpdateForm
    success_url= reverse_lazy('procesamientos_app:equipos')

#Autor: Daniel Castro Mercado
class EquiposDeleteView(LoginRequiredMixin,DeleteView):
    '''Vista para borrar equipos'''
    model = Equipos
    template_name = "procesamientos/equipos/delete_equipo.html"
    login_url=reverse_lazy('users_app:login')
    success_url= reverse_lazy('procesamientos_app:equipos')



