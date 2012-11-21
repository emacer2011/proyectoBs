#*-*coding: utf-8 --*-*
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

def login_user(request):
    estado = ""
    mensaje = ""
    username = password = ''
    next = request.REQUEST.get("next")
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if (next!=None):
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect("/")
            else:
                estado = "Cuenta Inactiva"
        else:
            estado ='alert alert-error'
            mensaje =" nombre de usuario o contraseña incorrecta."
    
    if (request.REQUEST.get("next")!=None):
                    estado='alert alert-error'
                    mensaje="Por favor iniciar sesion para poder continuar..."
    
    return render_to_response('login.html',{'mensaje':mensaje, 'estado':estado, 'next': next},context_instance=RequestContext(request))    
        
@login_required(login_url='/login')
def deslogear(request):
    logout(request)
    return HttpResponseRedirect("/login")


@login_required(login_url='/login')
def index(request):
    """docstring for index"""
    return render_to_response('menuPrincipal.html',context_instance=RequestContext(request)) 

@login_required(login_url='/login')
def altaDeposito(request):
    """docstring for altaDeposito"""
    deposito = Deposito()
    rubros = Rubro.objects.all()
    estado = ''
    mensaje=''
    if request.POST:
        deposito.direccion= request.POST.get('direccionDeposito')
        deposito.telefono= request.POST.get('telefonoDeposito')
        deposito.rubro= Rubro.objects.get(pk= request.POST.get('rubroDeposito'))
        deposito.save()
        mensaje='Deposito dado de alta con direccion: '+deposito.direccion
        estado='alert alert-success'
    return render_to_response('gstDeposito/altaDeposito.html',{'estado':estado, 'rubros':rubros, 'mensaje': mensaje},context_instance=RequestContext(request))

@login_required(login_url='/login')
def listarDeposito(request):
    """docstring for listarDeposito"""
    depositos = Deposito.objects.all()
    return render_to_response('gstDeposito/listarDeposito.html',{'depositos':depositos},context_instance=RequestContext(request)) 

# =========
# = Venta =
# =========

def venta(request):
    """docstring for venta"""
    return render_to_response('venta.html',context_instance=RequestContext(request)) 