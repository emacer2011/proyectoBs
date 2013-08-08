# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito, Producto, TipoProducto, Stock, NotaVenta, DetalleNotaVenta, NoFraccionable, Remito, DetalleFactura, Factura, DetalleRemito
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from misExcepciones import *
from datetime import *
from django.db import transaction
# ==================
# = Funciones Ajax =
# ==================

def cargarDetalles(request):
    """docstring for cargarDetalle"""
    detalles = DetalleRemito.objects.filter(remito = request.GET.get('pkRemito'))              
    mensaje = '<table>'
    mensaje = mensaje + "<th></th>"
    mensaje = mensaje + "<th>Producto</th>"
    mensaje = mensaje + "<th>Cantidad</th>"
    mensaje = mensaje + "<th>Entregado</th>"
    for detalle in detalles:
        mensaje = mensaje + "<tr>"
        mensaje = mensaje + '<td style="visibility:hidden" id = "pkDetalle">'+ str(detalle.pk)+'</td>'
        mensaje = mensaje + "<td>" + detalle.producto.nombre+ "</td>"
        mensaje = mensaje + "<td>" + str(detalle.cantidad)+ "</td>"
        if detalle.entregado:
            entregado = "checked DISABLED"
        else:
            entregado = ""
        pk = str(detalle.pk)
        mensaje = mensaje + '<td><input type="checkbox" onClick="cargarEntregados('+pk+')" name="entregado'+str(detalle.pk)+'" '+str(entregado)+'> </td>'
        mensaje = mensaje +"</tr>"
    mensaje = mensaje+"</table>"
    return HttpResponse(mensaje)

def cargarEntregados(request):
    """docstring for cargarEntregados"""
    pkDetalle = request.GET.get('pkDetalle')
    detalle = DetalleRemito.objects.get(pk = pkDetalle )
    entregado = not detalle.entregado
    detalle.entregado = entregado
    detalle.confirmarStock()
    detalle.save()  
    return HttpResponseRedirect("/cargarDetalles")

def actualizarEntregados(request):
    pkRemito = request.GET.get('pkRemito')
    remito = Remito.objects.get(pk = pkRemito )
    remito.actualizarEntregados()
    return HttpResponseRedirect("/cargarDetalles")

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
@transaction.commit_on_success
@login_required(login_url='/login')
def altaDeposito(request):
    """docstring for altaDeposito"""
    deposito = Deposito()
    rubros = Rubro.objects.all()
    estado = ''
    mensaje=''
    if request.POST:
        deposito.setDireccion(request.POST.get('direccionDeposito'))
        deposito.setTelefono(request.POST.get('telefonoDeposito'))
        deposito.setRubro(request.POST.get('rubroDeposito'))
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
@transaction.commit_on_success
def bajaDeposito(request):
    """docstring for bajaDeposito"""
    estado = ""
    mensaje = ""
    depositos = Deposito.objects.all()
    if request.is_ajax():
        if request.GET:
            pk = request.GET.get('pkDeposito')
            deposito = Deposito.objects.get(pk = pk )
            mensaje='Deposito con direccion: '+deposito.direccion+" eliminado"
            estado='alert alert-success'
            deposito.eliminarDeposito()
            return HttpResponse(str(estado)+"/"+str(mensaje))
    return render_to_response('gstDeposito/bajaDeposito.html',{'depositos':depositos, 'mensaje': mensaje, 'estado': estado},context_instance=RequestContext(request)) 

@login_required(login_url='/login')
@transaction.commit_on_success
def modificarDeposito(request):
    """docstring for modificarDeposito"""
    depositos = Deposito.objects.all()
    rubros = Rubro.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        deposito = Deposito.objects.get(pk = request.POST.get('pkDeposito') )
        deposito.setDireccion(request.POST.get('direccionDeposito'))
        deposito.setTelefono(request.POST.get('telefonoDeposito'))
        deposito.setRubro(request.POST.get('rubroDeposito'))
        deposito.save()
        mensaje='Deposito Modficiado con direccion: '+deposito.direccion
        estado='alert alert-success'
        
    return render_to_response('gstDeposito/modificarDeposito.html',{'depositos':depositos, 'rubros':rubros, 'mensaje': mensaje, 'estado': estado},context_instance=RequestContext(request)) 


# =========
# = Venta =
# =========
@transaction.commit_on_success
@login_required(login_url='/login')
def venta(request):
    """docstring for venta"""
    productos = Producto.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        productos = Producto.objects.all()
        notaVenta= NotaVenta()
        notaVenta.setNombre(request.POST.get("nombrePersona"))
        notaVenta.setApellido(request.POST.get("apellidoPersona"))
        notaVenta.setFecha(date.today())
        notaVenta.setPrecioTotal(0)
        notaVenta.setFacturada(False)
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
            #TODO: producto.vender devuelve mal la lista de stocks afectados!
            stocks = listaStock.keys()
            #import pdb # DEBUGGER
            #pdb.set_trace()# DEBUGGER
            for stock in stocks:
                detalle = DetalleNotaVenta()
                detalle.setProducto(stock.getProducto())
                detalle.setCantidad(listaStock[stock])
                detalle.setSubTotal(producto.getPrecio() * detalle.getCantidad())
                detalle.setDeposito(stock.getDeposito())
                detalle.setNota(notaVenta)
                detalle.save()
                mensaje ="Venta Realizada Con Exito" 
                estado = 'alert alert-success'
                notaVenta.incrementarTotal(detalle.getSubTotal())
        notaVenta.save()
                
    return render_to_response('venta.html',{'productos':productos,'estado': estado, 'mensaje':mensaje},context_instance=RequestContext(request)) 

# ================
# = Cargar Stock =
# ================
@transaction.commit_on_success
@login_required(login_url='/login')
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
        Stock.cargarStock(disponibles,deposito, producto)
        producto.setCantidad(producto.cantidad + disponibles)
        producto.save()
        mensaje='Se agrega '+str(disponibles) +' del producto '+producto.nombre+' en el deposito de '+deposito.direccion
        estado='alert alert-success'
        
    return render_to_response('cargarStock.html',{'mensaje':mensaje, 'estado':estado, 'productos':productos,'depositos':depositos},context_instance=RequestContext(request)) 

# =======================
# = Gestion de Producto =
# =======================
@transaction.commit_on_success
@login_required(login_url='/login')
def altaProducto(request):
    """docstring for altaProducto"""
    tipoProductos =TipoProducto.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        producto= Producto()
        producto.setNombre(request.POST.get("nombreProducto"))
        producto.setDescripcion(request.POST.get("descripcionProducto"))
        producto.tipoProducto = TipoProducto.objects.get(pk = request.POST.get("tipoProducto"))
        producto.setPrecio(request.POST.get("precioProducto"))
        producto.setCantidad(0)
        producto.estrategiaVenta = NoFraccionable.objects.get(pk = 0)
        producto.save()
        mensaje='Producto dado de alta con nombre: ' + producto.nombre
        estado='alert alert-success'
    return render_to_response('gstProducto/altaProducto.html',{'estado':estado, 'mensaje':mensaje, 'tipoProductos':tipoProductos},context_instance=RequestContext(request)) 
    
@transaction.commit_on_success
@login_required(login_url='/login')    
def bajaProducto(request):
    """docstring for bajaProducto"""
    mensaje = ""
    estado = ""
    productos = Producto.objects.all()
    if request.is_ajax():
        producto = Producto.objects.get(pk =request.GET.get("pkProducto") )
        if producto.puedeBorrarse():
            mensaje="Producto Eliminado"
            estado='alert alert-success'
            producto.delete()
        else:
            mensaje="No se pudo Eliminar porque tiene stocks relacionados"
            estado='alert alert-error'
        return HttpResponse(str(estado)+"/"+str(mensaje))
    return render_to_response('gstProducto/bajaProducto.html',{'estado':estado, 'mensaje':mensaje, 'productos':productos},context_instance=RequestContext(request)) 

@transaction.commit_on_success
@login_required(login_url='/login')        
def modificarProducto(request):
    """docstring for altaProducto"""
    tipoProductos = TipoProducto.objects.all()
    productos = Producto.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        try:
            producto= Producto.objects.get(pk = request.POST.get("pkProducto"))
            producto.nombre = request.POST.get("nombreProducto")
            if producto.nombre == "":
                raise ErrorProducto
            producto.descripcion = request.POST.get("descripcionProducto")
            producto.tipoProducto = TipoProducto.objects.get(pk = request.POST.get("tipoProducto"))
            if (producto.tipoProducto == None):
                raise ErrorProducto
            producto.precio = request.POST.get("precioProducto")
            if int(producto.precio) <= 0:
                raise ErrorProducto
            producto.cantidad = 0
            producto.estrategiaVenta = NoFraccionable.objects.get(pk = 0)
            producto.save()
            mensaje='Producto dado de alta con nombre: ' + producto.nombre
            estado='alert alert-success'
        except ErrorProducto:
            mensaje='Error al cargar los datos, por favor verifique el correcto ingreso de los mismos'
            estado='alert alert-error'
    return render_to_response('gstProducto/modificarProducto.html',{'estado':estado, 'mensaje':mensaje, 'tipoProductos':tipoProductos, 'productos': productos},context_instance=RequestContext(request)) 

@login_required(login_url='/login')
def listarProducto(request):
    """docstring for listarProducto"""
    productos = Producto.objects.all()
    return render_to_response('gstProducto/listarProducto.html',{'productos':productos},context_instance=RequestContext(request)) 

# ======================
# = Entrega Materiales =
# ======================
@transaction.commit_on_success
@login_required(login_url='/login')
def entregaMateriales(request):
    """docstring for entregaMateriales"""
    remitos = Remito.objects.filter(entregadoCompleto = False)
    detallesRemitos = DetalleRemito.objects.filter(entregado = False)       
    return render_to_response('entregaMateriales.html',{'remitos':remitos, 'detalles':detallesRemitos},context_instance=RequestContext(request)) 
    
# =====================
# = Cobro de Facturas =
# =====================
@transaction.commit_on_success
@login_required(login_url='/login')
def cobro(request):
    """docstring for cobro"""
    notas = NotaVenta.objects.filter(facturada = False)
    if request.POST:
        notaVenta=  NotaVenta.objects.get(pk = request.POST.get("nroNota"))
        notaVenta.facturada = True
        formaPago = request.POST.get("formaPago")
        precio = request.POST.get("precioNota")
        factura = Factura()
        factura.fecha=date.today()
        factura.precioTotal = precio
        factura.ventaNota = notaVenta
        factura.save()
        detalles  = DetalleNotaVenta.objects.filter(nota = notaVenta)
        for detalle in detalles:
            detalleFactura = DetalleFactura()
            detalleFactura.detalleNotaVenta = detalle
            detalleFactura.factura = factura
            detalleFactura.producto = detalle.producto
            detalleFactura.cantidad = detalle.cantidad
            detalleFactura.subtotal = detalle.subtotal
            detalleFactura.save()
            try:
                remito = Remito.objects.get(factura = factura, deposito = detalle.deposito )
            except ObjectDoesNotExist: 
                remito = Remito()
                remito.factura = factura
                remito.deposito = detalle.deposito
                remito.entregadoCompleto = False
                remito.save()
            detalleRemito = DetalleRemito()
            detalleRemito.cantidad = detalleFactura.cantidad
            detalleRemito.entregado = False
            detalleRemito.detalleFactura = detalleFactura
            detalleRemito.remito = remito
            detalleRemito.producto = detalleFactura.producto
            detalleRemito.deposito = detalle.deposito
            detalleRemito.save()

            stock= Stock.objects.get(producto=detalle.getProducto(), deposito=detalle.getDeposito())
            stock.reservadosNoConfirmados -= detalle.getCantidad()
            stock.reservadosConfirmados += detalle.getCantidad()
            stock.save()
        notaVenta.save()
    return render_to_response('cobro.html',{'notas':notas},context_instance=RequestContext(request))
