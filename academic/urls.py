from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    path('titulaciones/', views.lista_titulaciones, name='titulaciones'),
]