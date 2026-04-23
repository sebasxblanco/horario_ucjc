from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    path('titulaciones/',                          views.lista_titulaciones,  name='titulaciones'),
    path('asignaturas/<int:pk>/editar/',           views.editar_asignatura,   name='editar_asignatura'),
    path('asignaturas/<int:pk>/eliminar/',         views.eliminar_asignatura, name='eliminar_asignatura'),
]
