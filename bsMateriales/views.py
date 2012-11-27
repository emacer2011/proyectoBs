#*-*coding: utf-8 --*-*
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito, Producto, TipoProducto, Stock, NotaVenta, DetalleNotaVenta, NoFraccionable
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from datetime import *
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
        notaVenta= NotaVenta()
        notaVenta.nombre_cliente = request.POST.get("nombrePersona")
        notaVenta.apellido_cliente = request.POST.get("apellidoPersona")
        notaVenta.fecha = date.today()
        notaVenta.save()
        palabra = request.POST.get("productos")
        palabraParse = str(palabra).split(",")
        dic =  {}
        for i in palabraParse :
            claveValor = i.split("=")
            dic[Producto.objects.get(pk = claveValor[0])] = claveValor[1]
        productos =dic.keys()
        for producto in productos:
            listaStock = producto.vender(cantidad = dic[producto])
            stocks = listaStock.keys()
            for stock in stocks:
                detalle = DetalleNotaVenta()
                detalle.producto = stock.producto
                detalle.cantidad = listaStock[stock]
                detalle.subtotal = producto.precio * detalle.cantidad
                detalle.deposito = stock.deposito
                detalle.nota = notaVenta
                detalle.save()
        
    return render_to_response('venta.html',{'productos':productos},context_instance=RequestContext(request)) 
    
# ================
# = Cargar Stock =
# ================
def cargarStock(request):
    """docstring for cargarStock"""
    productos = Producto.objects.all()
    depositos = Deposito.objects.all()
    mensaje = ""
    estado= ""
    if request.POST:
        producto =Producto.objects.get(pk = request.POST.get("pkProducto"))
        disponibles = int(request.POST.get("disponible"))
        deposito=Deposito.objects.get(pk =request.POST.get("deposito"))
        stock = Stock()
        stock.nuevoStock(disponibles,deposito, producto)
        producto.cantidad = producto.cantidad + disponibles
        producto.save()
        mensaje='Se agrega '+str(disponibles) +' del producto '+producto.nombre+' en el deposito de '+deposito.direccion
        estado='alert alert-success'
    return render_to_response('cargarStock.html',{'mensaje':mensaje, 'estado':estado, 'productos':productos,'depositos':depositos},context_instance=RequestContext(request)) 


def altaProducto(request):
    """docstring for altaProducto"""
    tipoProductos =TipoProducto.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        producto= Producto()
        producto.nombre = request.POST.get("nombreProducto")
        producto.descripcion = request.POST.get("descripcionProducto")
        producto.tipoProducto = TipoProducto.objects.get(pk = request.POST.get("tipoProducto"))
        producto.precio = request.POST.get("precioProducto")
        producto.cantidad = 0
        producto.estrategiaVenta = NoFraccionable.objects.get(pk = 0)
        producto.save()
        mensaje='Producto dado de alta con nombre: ' + producto.nombre
        estado='alert alert-success'
    return render_to_response('gstProducto/altaProducto.html',{'estado':estado, 'mensaje':mensaje, 'tipoProductos':tipoProductos},context_instance=RequestContext(request)) 