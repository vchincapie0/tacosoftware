from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import csv
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Importacion de modelos y formularios
from .models import Proveedores, ProveedoresAudit
from .forms import ProveedorCreateForm, ProveedoresUpdateForm, ProveedorAuditFilterForm

class ProveedoresListView(LoginRequiredMixin, ListView):
    '''Clase para mostrar los datos de los proveedores'''
    model = Proveedores
    template_name = "proveedores/list_proveedor.html"
    login_url=reverse_lazy('users_app:login')
    paginate_by=10
    context_object_name = 'proveedor'

    def get_queryset(self):
        '''Funcion que toma de la barra de busqueda la pablabra clave para filtrar'''
        palabra_clave= self.request.GET.get("kword",'')
        lista = Proveedores.objects.filter(
            prov_nombre__icontains = palabra_clave,
            deleted=False  # Solo proveedores activos
        ).order_by('prov_nombre')  # Ordenar por 'prov_nombre'
        return lista
    
class ProveedoresCreateView(LoginRequiredMixin,CreateView):
    '''Clase para crear nuevos proveedores'''
    model = Proveedores
    template_name = "proveedores/add_proveedor.html"
    login_url=reverse_lazy('home_app:home')
    #Campos que se van a mostrar en el formulario
    form_class = ProveedorCreateForm
    #url donde se redirecciona una vez acaba el proceso el "." es para redireccionar a la misma pagina
    success_url= reverse_lazy('proveedores_app:list_proveedores') 

    def form_valid(self, form):
        #Obtener los datos del fomulario
        nombre = form.cleaned_data['prov_nombre']

        # Agregar un mensaje de éxito con el nombre de usuario
        messages.success(self.request, f'¡El proveedor {nombre} se ha agregado correctamente!')

        return super(ProveedoresCreateView, self).form_valid(form)

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    '''Vista para actualizar los datos de proveedores'''
    model = Proveedores
    template_name = "proveedores/edit_proveedor.html"
    login_url=reverse_lazy('users_app:login')
    form_class=ProveedoresUpdateForm
    success_url= reverse_lazy('proveedores_app:list_proveedores')

    def form_valid(self, form):
        #Obtener los datos del fomulario
        nombre = form.cleaned_data['prov_nombre']

        # Agregar un mensaje de éxito con el nombre de usuario
        messages.success(self.request, f'¡El proveedor {nombre} se ha actualizado correctamente!')

        return super(ProveedorUpdateView, self).form_valid(form)

class ProveedoresDeleteView(LoginRequiredMixin, DeleteView):
    '''Vista para borrar Proveedores'''
    model = Proveedores
    template_name = "proveedores/delete_proveedor.html"
    login_url=reverse_lazy('users_app:login')
    success_url= reverse_lazy('proveedores_app:list_proveedores')

class ProveedoresAuditListView(LoginRequiredMixin, ListView):
    '''Clase para mostrar los datos de logs de proveedores'''
    model = ProveedoresAudit
    template_name = "administrador/auditorias/proveedoraudit.html"
    login_url=reverse_lazy('users_app:login')
    paginate_by=10
    context_object_name = 'proveedor'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener los parámetros de filtrado del formulario
        form = ProveedorAuditFilterForm(self.request.GET)

        # Aplicar filtros si el formulario es válido
        if form.is_valid():
            proveedor = form.cleaned_data.get('proveedor')
            action = form.cleaned_data.get('action')
            changed_by = form.cleaned_data.get('changed_by')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Filtrar por usuario, acción, usuario que realizó el cambio y rango de fechas
            if proveedor:
                queryset = queryset.filter(proveedor=proveedor)
            if action:
                queryset = queryset.filter(action=action)
            if changed_by:
                queryset = queryset.filter(changed_by=changed_by)
            if start_date:
                queryset = queryset.filter(changed_at__gte=start_date)
            if end_date:
                # Agregar 1 día a la fecha final para incluir todos los registros de ese día
                end_date += timezone.timedelta(days=1)
                queryset = queryset.filter(changed_at__lt=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProveedorAuditFilterForm(self.request.GET)
        return context
    
def export_proveedores_to_excel(request):
    '''Vista para exportar datos de tabla proveedores en formato excel'''
    # Obtener la fecha y hora actual
    fecha_descarga = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obtener los datos de proveedores que quieres exportar
    proveedores = Proveedores.objects.filter(deleted=False)  # Filtrar proveedores activos

    # Crear un nuevo libro de Excel y una hoja de trabajo
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Proveedores'

    # Establecer estilos para la primera línea (encabezado personalizado)
    title_font = Font(bold=True)
    title_fill = PatternFill(start_color="FFFFFF00", end_color="FFFFFF00", fill_type="solid")  # Transparente
    title_alignment = Alignment(horizontal='center')
    
    # Agregar fila de título personalizado
    worksheet.append(['TACO MAS'])  # Agregar texto del título
    worksheet.merge_cells('A1:C1')  # Combinar celdas para el título
    title_cell = worksheet['A1']
    title_cell.font = title_font
    title_cell.fill = title_fill
    title_cell.alignment = title_alignment

    # Agregar información adicional (fecha y nombre del software) en una nueva fila
    worksheet.append(['Fecha de descarga:', fecha_descarga])
    worksheet.append(['Software:', 'Tacosoft'])

    # Agregar espacio en blanco entre la información adicional y los encabezados
    worksheet.append([])  # Agregar una fila vacía

    # Agregar encabezados a la siguiente fila
    headers = ['NIT', 'Razón Social', 'Teléfono']
    worksheet.append(headers)

    # Aplicar estilos a la fila de encabezados (fila actual + 2)
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")  # Gris claro
    header_alignment = Alignment(horizontal='center')

    for col in range(1, len(headers) + 1):
        header_cell = worksheet.cell(row=worksheet.max_row, column=col)
        header_cell.font = header_font
        header_cell.fill = header_fill
        header_cell.alignment = header_alignment

    # Agregar datos de proveedores a las siguientes filas
    for proveedor in proveedores:
        data_row = [proveedor.nit, proveedor.prov_nombre, proveedor.prov_telefono]
        worksheet.append(data_row)

    # Crear una respuesta HTTP con el archivo Excel como contenido
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proveedores.xlsx'

    # Guardar el libro de Excel en la respuesta HTTP
    workbook.save(response)

    return response

def export_proveedores_to_csv(request):
    '''Vista para exportar datos de tabla proveedores en formato CSV'''
    proveedores = Proveedores.objects.filter(deleted=False)  # Obtener datos de proveedores
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=proveedores.csv'

    writer = csv.writer(response)
    writer.writerow(['NIT', 'Razón Social', 'Teléfono'])  # Encabezados de columnas

    for proveedor in proveedores:
        writer.writerow([proveedor.nit, proveedor.prov_nombre, proveedor.prov_telefono])

    return response