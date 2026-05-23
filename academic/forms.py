from django import forms
from .models import Asignatura


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'codigo', 'curso', 'semestre',
                  'horas_sesion', 'sesiones_semana', 'es_compartida', 'matriculados']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
                'placeholder': 'Nombre de la asignatura',
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
                'placeholder': 'Ej: INF101',
            }),
            'curso': forms.Select(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
            }),
            'semestre': forms.Select(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
            }),
            'horas_sesion': forms.NumberInput(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
                'min': 1, 'max': 4,
            }),
            'sesiones_semana': forms.NumberInput(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
                'min': 1, 'max': 5,
            }),
            'es_compartida': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-stroke bg-raised text-burg '
                         'focus:ring-burg focus:ring-1',
            }),
            'matriculados': forms.NumberInput(attrs={
                'class': 'w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
                         'text-sm text-ink focus:outline-none focus:border-burg '
                         'focus:ring-1 focus:ring-burg transition-colors',
                'min': 0,
            }),
        }
