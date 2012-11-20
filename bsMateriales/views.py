#*-*coding: utf-8 --*-*
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito

def index(request):
    """docstring for index"""
    return render_to_response('menuPrincipal.html',context_instance=RequestContext(request)) 
    

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

def listarDeposito(request):
    """docstring for listarDeposito"""
    depositos = Deposito.objects.all()
    return render_to_response('gstDeposito/listarDeposito.html',{'depositos':depositos},context_instance=RequestContext(request)) 