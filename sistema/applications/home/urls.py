from django.urls import path
from . import views

app_name='home_app'

urlpatterns = [
    path('home/',views.Home.as_view(),name='home'),
    path('audit_index/',views.AuditViews.as_view(),name='auditorias_index'),
    path('generic_index/',views.GenericsViews.as_view(),name='genericas_index'),
]