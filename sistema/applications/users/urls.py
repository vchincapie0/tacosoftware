#Fecha de Creación: 02/02/2024
#Autor: Vivian Carolina Hincapie Escobar
#Última modficación: 15/05/2024

from django.urls import path
from . import views
from .decorators import admin_required  # Importa el decorador personalizado

app_name='users_app'

urlpatterns = [
    path('',views.LogIn.as_view(),name='login'),
    path('list_user/',admin_required(views.UsersListView.as_view()),name='list_user'),
    path('user/export/xls',admin_required(views.export_users_to_excel), name='export_users_excel'),
    path('user/export/cvs',admin_required(views.export_users_to_csv), name='export_users_csv'),
    path('add_user/',admin_required(views.UserRegisterView.as_view()),name='add_user'),
    path('edit_user/<pk>',admin_required(views.UserUpdateView.as_view()),name='edit_user'),
    path('delete_user/<pk>',admin_required(views.UserDeleteView.as_view()),name='delete_user'),
    path('logout/',views.LogOut.as_view(),name='logout'),
    path('user_audit/',admin_required(views.UserAuditListView.as_view()),name='user_audit'),
]