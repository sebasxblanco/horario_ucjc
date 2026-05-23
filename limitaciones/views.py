from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Limitacion
from .forms import LimitacionForm


def _puede_ver(user):
    if user.is_superuser:
        return True
    return hasattr(user, 'rol') and user.rol in ('DECANO', 'IT', 'CONSULTOR', 'PROFESOR')


def _es_admin(user):
    if user.is_superuser:
        return True
    return hasattr(user, 'rol') and user.rol in ('DECANO', 'IT', 'CONSULTOR')


def _403(request):
    return HttpResponseForbidden(
        render(request, 'limitaciones/403.html', status=403).content
    )


# ── Lista ──────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def lista(request):
    if not _puede_ver(request.user):
        return _403(request)

    if _es_admin(request.user):
        qs = Limitacion.objects.select_related('profesor', 'asignatura', 'bloque')
    else:
        qs = Limitacion.objects.filter(profesor=request.user).select_related('asignatura', 'bloque')

    estado_filtro = request.GET.get('estado', '')
    tipo_filtro   = request.GET.get('tipo', '')
    if estado_filtro:
        qs = qs.filter(estado=estado_filtro)
    if tipo_filtro:
        qs = qs.filter(tipo=tipo_filtro)

    pendientes = qs.filter(estado=Limitacion.Estado.PENDIENTE).count() if _es_admin(request.user) else 0

    return render(request, 'limitaciones/lista.html', {
        'limitaciones':  qs,
        'estado_filtro': estado_filtro,
        'tipo_filtro':   tipo_filtro,
        'estados':       Limitacion.Estado.choices,
        'tipos':         Limitacion.Tipo.choices,
        'es_admin':      _es_admin(request.user),
        'pendientes':    pendientes,
    })


# ── Crear ──────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def crear(request):
    if not _puede_ver(request.user):
        return _403(request)

    if request.method == 'POST':
        form = LimitacionForm(request.POST)
        if form.is_valid():
            lim = form.save(commit=False)
            lim.profesor = request.user
            lim.save()
            messages.success(request, 'Limitación notificada al decano correctamente.')
            return redirect('limitaciones:lista')
    else:
        form = LimitacionForm()

    return render(request, 'limitaciones/crear.html', {'form': form})


# ── Detalle ────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def detalle(request, pk):
    lim = get_object_or_404(Limitacion, pk=pk)

    if not _es_admin(request.user) and lim.profesor != request.user:
        return _403(request)

    return render(request, 'limitaciones/detalle.html', {
        'lim':      lim,
        'estados':  Limitacion.Estado.choices,
        'es_admin': _es_admin(request.user),
    })


# ── Gestionar estado (solo decano/admin) ───────────────────────────────────

@login_required(login_url='/accounts/login/')
def gestionar(request, pk):
    if not _es_admin(request.user):
        return _403(request)

    if request.method != 'POST':
        return redirect('limitaciones:detalle', pk=pk)

    lim          = get_object_or_404(Limitacion, pk=pk)
    nuevo_estado = request.POST.get('estado', '').strip()
    respuesta    = request.POST.get('respuesta_decano', '').strip()

    estados_validos = [e[0] for e in Limitacion.Estado.choices]
    if nuevo_estado in estados_validos:
        lim.estado = nuevo_estado
    if respuesta:
        lim.respuesta_decano = respuesta
    lim.save()

    messages.success(request, f'Limitación actualizada a «{lim.get_estado_display()}».')
    return redirect('limitaciones:detalle', pk=pk)
