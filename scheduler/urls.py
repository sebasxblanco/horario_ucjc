from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('',                         views.lista,          name='lista'),
    path('generar/',                 views.generar,        name='generar'),
    path('horario/<int:pk>/',        views.detalle,        name='detalle'),
    path('horario/<int:pk>/estado/', views.cambiar_estado, name='cambiar_estado'),
    path('horario/<int:pk>/eliminar/', views.eliminar,     name='eliminar'),
    path('limpiar/',                   views.limpiar,       name='limpiar'),
]
