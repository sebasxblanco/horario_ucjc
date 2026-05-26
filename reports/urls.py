from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('',                     views.index,         name='index'),
    path('<int:pk>/pdf/',        views.exportar_pdf,  name='pdf'),
    path('<int:pk>/excel/',      views.exportar_excel, name='excel'),
]
