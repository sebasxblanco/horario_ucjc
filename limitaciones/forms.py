from django import forms
from .models import Limitacion
from academic.models import BloqueHorario

_INPUT = ('w-full bg-raised border border-stroke rounded-lg px-4 py-2.5 '
          'text-sm text-ink focus:outline-none focus:border-burg '
          'focus:ring-1 focus:ring-burg transition-colors')


class LimitacionForm(forms.ModelForm):
    class Meta:
        model  = Limitacion
        fields = ['asignatura', 'fecha', 'bloque', 'tipo', 'descripcion']
        widgets = {
            'asignatura': forms.Select(attrs={'class': _INPUT}),
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': _INPUT},
                format='%Y-%m-%d'
            ),
            'bloque': forms.Select(attrs={'class': _INPUT}),
            'tipo': forms.Select(attrs={'class': _INPUT}),
            'descripcion': forms.Textarea(attrs={
                'class': _INPUT + ' resize-none',
                'rows': 4,
                'placeholder': 'Describe el problema con el mayor detalle posible…',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asignatura'].required = False
        self.fields['asignatura'].empty_label = '— Sin asignatura específica —'
        self.fields['bloque'].required = False
        self.fields['bloque'].empty_label = '— Sin bloque específico —'
        self.fields['bloque'].queryset = BloqueHorario.objects.filter(activo=True).order_by('hora_inicio')
