# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from bsMateriales.models import Rubro, Deposito, Producto, TipoProducto, Stock, NotaVenta, DetalleNotaVenta, NoFraccionable, Remito, DetalleFactura, Factura, DetalleRemito,Fraccionable
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

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
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
        mensaje = mensaje + "<td>" + detalle.producto.getNombre()+ "</td>"
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

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
def cargarEntregados(request):
    """docstring for cargarEntregados"""
    pkDetalle = request.GET.get('pkDetalle')
    detalle = DetalleRemito.objects.get(pk = pkDetalle )
    entregado = not detalle.entregado
    detalle.entregado = entregado
    detalle.confirmarStock()
    detalle.save()  
    return HttpResponseRedirect("/cargarDetalles")

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
def actualizarEntregados(request):
    pkRemito = request.GET.get('pkRemito')
    remito = Remito.objects.get(pk = pkRemito )
    remito.actualizarEntregados()
    return HttpResponseRedirect("/cargarDetalles")

# ==========================================================================================================
# ==========================================================================================================
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
def cargarDepositos(request):
    """docstring for cargarDepositos"""
    pkProducto = request.GET.get('pkProducto')
    deposito = Deposito.objects.get(pk = request.POST.get('pkDeposito') )
#    detalle = DetalleRemito.objects.get(pk = pkDetalle )
#    entregado = not detalle.entregado
#    detalle.entregado = entregado
#    detalle.confirmarStock()
#    detalle.save()  
    return HttpResponseRedirect("/cargarDetalles")

# ==========================================================================================================
# ==========================================================================================================


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
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
@transaction.commit_on_success
@login_required(login_url='/login')
def altaDeposito(request):
    """docstring for altaDeposito"""
    deposito = Deposito()
    rubros = Rubro.objects.all()
    estado = ''
    mensaje=''
    if request.POST:
        deposito.inicializar(request.POST.get('direccionDeposito'),request.POST.get('telefonoDeposito'),request.POST.get('rubroDeposito'))
        deposito.save()
        mensaje='Deposito dado de alta con direccion: '+deposito.getDireccion()
        estado='alert alert-success'
    return render_to_response('gstDeposito/altaDeposito.html',{'estado':estado, 'rubros':rubros, 'mensaje': mensaje},context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
@login_required(login_url='/login')
def listarDeposito(request):
    """docstring for listarDeposito"""
    depositos = Deposito.objects.all()
    return render_to_response('gstDeposito/listarDeposito.html',{'depositos':depositos},context_instance=RequestContext(request)) 

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
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
            mensaje='Deposito con direccion: '+deposito.getDireccion()+" eliminado"
            estado='alert alert-success'
            deposito.eliminarDeposito()
            return HttpResponse(str(estado)+"/"+str(mensaje))
    return render_to_response('gstDeposito/bajaDeposito.html',{'depositos':depositos, 'mensaje': mensaje, 'estado': estado},context_instance=RequestContext(request)) 

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
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
        deposito.inicializar(request.POST.get('direccionDeposito'),request.POST.get('telefonoDeposito'),request.POST.get('rubroDeposito'))
        deposito.save()
        mensaje='Deposito Modficiado con direccion: '+deposito.getDireccion()
        estado='alert alert-success'
        
    return render_to_response('gstDeposito/modificarDeposito.html',{'depositos':depositos, 'rubros':rubros, 'mensaje': mensaje, 'estado': estado},context_instance=RequestContext(request)) 


# =========
# = Venta =
# =========
@transaction.commit_on_success
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
@login_required(login_url='/login')
def venta(request):
    """docstring for venta"""
    productos = Producto.objects.all()
    productos = filter(lambda x: x.getCantidad() != 0 , productos)
    mensaje = ""
    estado = ""
    if request.POST:
        productos = Producto.objects.all()
        notaVenta= NotaVenta()
        notaVenta.inicializar(request.POST.get("nombrePersona"), request.POST.get("apellidoPersona"))
        notaVenta.save()

        #PROCESA ENTRADAS DE LOS DATOS
        palabra = request.POST.get("productos")
        palabraParse = str(palabra).split(",")
        dic =  {}
        for i in palabraParse :    
            claveValor = i.split("=")
            
            producto = Producto.objects.get(pk = claveValor[0])
            listaStock=producto.vender(cantidad= claveValor[1], fraccion = claveValor[2])
            if claveValor[2] == '-':
                claveValor[2] = 1 
            stocks = listaStock.keys()
            for stock in stocks:
                detalle = DetalleNotaVenta()
                detalle.inicializar(stock.getProducto(),listaStock[stock],((producto.getPrecio() * listaStock[stock])*float(claveValor[2])), stock.getDeposito(),notaVenta)
                detalle.save()
                notaVenta.incrementarTotal(detalle.getSubTotal())
                mensaje ="Venta Realizada Con Exito" 
                estado = 'alert alert-success'
        notaVenta.save()
                
    return render_to_response('venta.html',{'productos':productos,'estado': estado, 'mensaje':mensaje},context_instance=RequestContext(request)) 

# ================
# = Cargar Stock =
# ================
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
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
        producto.setCantidad(producto.getCantidad() + disponibles)
        producto.save()
        mensaje='Se agrega '+str(disponibles) +' del producto '+producto.getNombre()+' en el deposito de '+deposito.getDireccion()
        estado='alert alert-success'
        
    return render_to_response('cargarStock.html',{'mensaje':mensaje, 'estado':estado, 'productos':productos,'depositos':depositos},context_instance=RequestContext(request)) 

# =======================
# = Gestion de Producto =
# =======================
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
@transaction.commit_on_success
@login_required(login_url='/login')
def altaProducto(request):
    """docstring for altaProducto"""
    tipoProductos =TipoProducto.objects.all()
    mensaje = ""
    estado = ""
    if request.POST:
        producto= Producto()
        estrategiaVenta = ""
        if (request.POST.getlist('fraccionable') == []):
            print "NoFraccionable"
            estrategiaVenta = NoFraccionable.objects.get(pk = 0)
        else:
            print "Fraccionable"
            estrategiaVenta = Fraccionable()
            estrategiaVenta.setMedida(request.POST.get("medidaProducto"))
            estrategiaVenta.setMinimo(request.POST.get("medidaMinimaProducto"))
            estrategiaVenta.save()

        producto.inicializar(request.POST.get("nombreProducto"),request.POST.get("descripcionProducto"), TipoProducto.objects.get(pk = request.POST.get("tipoProducto")),request.POST.get("precioProducto"),estrategiaVenta)
        producto.save()
        
        mensaje='Producto dado de alta con nombre: ' + producto.getNombre()
        estado='alert alert-success'

        p1 = Producto.objects.get(pk= producto.pk)
    return render_to_response('gstProducto/altaProducto.html',{'estado':estado, 'mensaje':mensaje, 'tipoProductos':tipoProductos},context_instance=RequestContext(request)) 
    
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
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


@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
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
            producto.inicializar(request.POST.get("nombreProducto"),request.POST.get("descripcionProducto"), TipoProducto.objects.get(pk = request.POST.get("tipoProducto")),request.POST.get("precioProducto"),NoFraccionable.objects.get(pk = 0))
            producto.save()
            mensaje='Producto dado de alta con nombre: ' + producto.nombre
            estado='alert alert-success'
        except ErrorProducto:
            mensaje='Error al cargar los datos, por favor verifique el correcto ingreso de los mismos'
            estado='alert alert-error'
    return render_to_response('gstProducto/modificarProducto.html',{'estado':estado, 'mensaje':mensaje, 'tipoProductos':tipoProductos, 'productos': productos},context_instance=RequestContext(request)) 

@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
@login_required(login_url='/login')
def listarProducto(request):
    """docstring for listarProducto"""
    productos = Producto.objects.all()
    return render_to_response('gstProducto/listarProducto.html',{'productos':productos},context_instance=RequestContext(request)) 

# ======================
# = Entrega Materiales =
# ======================
@user_passes_test(lambda u: u.groups.filter(name='CAJERO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
@transaction.commit_on_success
@login_required(login_url='/login')
def entregaMateriales(request):
    """docstring for entregaMateriales"""
    remitos = Remito.objects.filter(entregadoCompleto = False)
    detallesRemitos = DetalleRemito.objects.filter(entregado = False)       
    return render_to_response('entregaMateriales.html',{'remitos':remitos, 'detalles':detallesRemitos},context_instance=RequestContext(request)) 
    
## =====================
# = Cobro de Facturas =
# =====================
@user_passes_test(lambda u: u.groups.filter(name='VENDEDORES').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ADMINISTRATIVO').count() == 0, login_url='/')
@user_passes_test(lambda u: u.groups.filter(name='ENCARGADO-DEPOSITO').count() == 0, login_url='/')
@transaction.commit_on_success
@login_required(login_url='/login')
def cobro(request):
    """docstring for cobro"""
    notas = NotaVenta.objects.filter(facturada = False)
    if request.POST:
        notaVenta =  NotaVenta.objects.get(pk = request.POST.get("nroNota"))
        notaVenta.facturada = True
        factura = Factura()
        factura.inicializar(request.POST.get("formaPago"), request.POST.get("precioNota"), notaVenta)
        factura.save()
        detalles  = DetalleNotaVenta.objects.filter(nota = notaVenta)
        for detalle in detalles:
            detalleFactura = DetalleFactura()
            detalleFactura.inicializar(detalle,factura,detalle.producto, detalle.cantidad, detalle.subtotal)
            detalleFactura.save()
            try:
                remito = Remito.objects.get(factura = factura, deposito = detalle.deposito )
            except ObjectDoesNotExist: 
                remito = Remito()
                remito.inicializar(factura, detalle.deposito)   
                remito.save()
            detalleRemito = DetalleRemito()
            detalleRemito.inicializar(detalleFactura.cantidad,detalleFactura,remito,detalleFactura.producto)
            detalleRemito.save()
            stock= Stock.objects.get(producto=detalle.getProducto(), deposito=detalle.getDeposito())
            stock.reservadosNoConfirmados -= detalle.getCantidad()
            stock.reservadosConfirmados += detalle.getCantidad()
            stock.save()
        notaVenta.save()
    return render_to_response('cobro.html',{'notas':notas},context_instance=RequestContext(request))
