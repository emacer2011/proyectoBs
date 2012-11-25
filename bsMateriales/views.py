#*-*coding: utf-8 --*-*
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito, Producto, TipoProducto, Stock
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# =======================
# = GESTION DE USUARIOS =
# =======================
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

# =====================
# = GESTION PRINCIPAL =
# =====================
@login_required(login_url='/login')
def index(request):
    """docstring for index"""
    return render_to_response('menuPrincipal.html',context_instance=RequestContext(request)) 

# ====================
# = GESTION DEPOSITO =
# ====================
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

@login_required(login_url='/login')
def bajaDeposito(request):
    """docstring for bajaDeposito"""
    depositos = Deposito.objects.all()
    return render_to_response('gstDeposito/bajaDeposito.html',{'depositos':depositos},context_instance=RequestContext(request)) 

# =========
# = Venta =
# =========
@login_required(login_url='/login')
def venta(request):
    """docstring for venta"""
    productos = Producto.objects.all()
    if request.POST:
        palabra = request.POST.get("productos")
        palabraParse = str(palabra).split(",")
        dic =  {}
        for i in palabraParse :
            claveValor = i.split("=")
            dic[claveValor[0]] = claveValor[1]
            print "producto:"+claveValor[0]+"y cantidad: "+claveValor[1]
                
    return render_to_response('venta.html',{'productos':productos},context_instance=RequestContext(request)) 
    
# ================
# = Cargar Stock =
# ================
def cargarStock(request):
    """docstring for cargarStock"""
    productos = Producto.objects.all()
    depositos = Deposito.objects.all()
    if request.POST:
        producto =Producto.objects.get(pk = request.POST.get("pkProducto"))
        disponibles = int(request.POST.get("disponible"))
        deposito=Deposito.objects.get(pk =request.POST.get("deposito"))
        stock = Stock()
        stock.nuevoStock(disponibles,deposito, producto)
        producto.cantidad = producto.cantidad + disponibles
        producto.save()
    return render_to_response('cargarStock.html',{'productos':productos,'depositos':depositos},context_instance=RequestContext(request)) 