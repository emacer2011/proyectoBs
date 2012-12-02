from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from misExcepciones import *
import re
# Create your models here.
# ===============
# = Clase Rubro =
# ===============

class Rubro(models.Model):
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank=True)
    
    def __unicode__(self):
        return "%s" % self.nombre
# ==================
# = Clase Deposito =
# ==================
class Deposito(models.Model):
    direccion = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 15)
    rubro = models.ForeignKey(Rubro)
    class Meta:
        permissions = (
            ("deposito", "Abm Depositos"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    def setDireccion(self, direccion):
        if re.match('\w+(\s\w+)*$', direccion):
            self.direccion = direccion
        else:
            raise ErrorDeposito()

    def setTelefono(self, telefono):
        if re.match('\d{7,13}$', telefono):
            self.telefono = telefono
        else:
            raise ErrorDeposito()

    def setRubro(self, pkRubro):
        try:
            unRubro = Rubro.objects.get(pk = pkRubro)        
            self.rubro = unRubro
        except ObjectDoesNotExist:
            raise ErrorDeposito()
    
    def __unicode__(self):
        return "%s" % self.direccion
        
# =======================
# = Clase Tipo Producto =
# =======================
class TipoProducto(models.Model):
    nombre = models.CharField(max_length = 40)
    unidadMedida = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank=True)
    rubro = models.ForeignKey(Rubro)    
    def __unicode__(self):
        return "%s" % self.nombre


# ====================
# = Estrategia Venta =
# ====================

ESTRATEGIA_NOFRACCIONABLE = 0

class EstrategiaVenta(models.Model):

    class Meta:
        abstract = True

    def vender(self, producto, cantidad, fraccion):
        raise NotImplemented    
        
# ==================
# = Clase Producto =
# ==================


class Producto(models.Model):
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank = True)
    tipoProducto = models.ForeignKey(TipoProducto)
    estrategiaVenta = models.ForeignKey('Fraccionable')
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    class Meta:
        permissions = (
            ("producto", "puede manejar abm Producto"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )

    def __unicode__(self):
        return "%s" % self.nombre

    def obtenerEstrategiaDeVenta(self):
        if self.estrategiaVenta.pk == ESTRATEGIA_NOFRACCIONABLE:
            return NoFraccionable.instance()
        return self.estrategiaVenta

    def verificarCantidadStock(self):
        stockList = self.stock_set.all()
        cantidad = 0
        for stock in stockList:
            cantidad += stock.disponibles
        return cantidad            

    def vender(self, cantidad = None, fraccion = 5):
        if (cantidad <= 0) or (catidad > self.verificarCantidadStock()):
            raise ErrorVenta()
        else:
            return self.obtenerEstrategiaDeVenta().vender(self, cantidad, fraccion)
        

# =================
# = Fraccionables =
# =================

class Fraccionable(EstrategiaVenta):
    medida = models.IntegerField()
    minimo = models.IntegerField()

    def vender(self, producto, cantidad, fraccion):
        stockLista = producto.stock_set.all()
        stockMinimo = None
        stockAfectados = {}
        ventaCompleta = False
        while not ventaCompleta:        
            if stockLista[0].disponibles > 0:
                stockMinimo = stockLista[0]        
            for elementoLista in stockLista:
                if stockMinimo != None:
                    if (elementoLista.disponibles != 0) and (elementoLista.disponibles < stockMinimo.disponibles):
                        stockMinimo = elementoLista
                    else:
                        continue
                elif elementoLista.disponibles > 0:
                    stockMinimo = elementoLista
            if stockMinimo.disponibles >= cantidad:
                producto = self.fraccionar(producto, fraccion, cantidad)
                stockAfectados[stockMinimo] = cantidad
            else:
                producto = self.fraccionar(producto, fraccion, stockMinimo.disponibles, stockMinimo)
                stockAfectados[stockMinimo] = cantidad - stockMinimo.disponibles
                prod = self.vender(producto, cantidad = cantidad - stockMinimo.disponibles, fraccion = fraccion)
            producto.save()
        return stockAfectados

    def fraccionar(self, producto, fraccion, cantidad, stockMinimo = None):
        print fraccion
        descrip = "tiene medida: " + str(self.medida - fraccion)
        resto = self.medida - fraccion
        if resto > self.minimo:
          	estrategiaVenta = Fraccionable(medida = resto, minimo = self.minimo)
        else:
            estrategiaVenta = NoFraccionable.instance()
        
        pSobra, created = Producto.objects.get_or_create(nombre = producto.nombre, descripcion = descrip, default = {
                        'nombre': producto.nombre,
                        'descripcion': descrip,
                        'tipoProducto': producto.tipoProducto,
                        'estrategiaVenta': estrategiaVenta
                        })
        if created:
            stock = Stock()
            stock.reservadosConfirmados = 0
            stock.reservadosNoConfirmados = 0
            stock.disponibles = cantidad
            stock.deposito = stockMinimo.deposito
            stock.producto = pSobra
            stock.save()
        else:
            stock, created = Stock.objects.get_or_create(producto = prod, deposito = stockMinimo.deposito, default = {
                             'reservadosConfirmados' : 0,
                             'reservadosNoConfirmados' : 0,
            				 'disponibles' : cantidad,
            				 'deposito' : stockMinimo.deposito,
            				 'producto' : pSobra
                             })
            if not created:            
                stock.disponibles = stock.disponibles + cantidad
                stock.save()
    
        descrip = "tiene medida: " + str(fraccion)
        pVenta, created = Producto.objects.get_or_create(nombre = producto.nombre, descripcion = descrip, default = {
                        'nombre' : producto.nombre,
                        'descripcion' : "tiene medida: " + str(fraccion),
                        'tipoProducto' : producto.tipoProducto,
                        'estrategiaVenta' : NoFraccionable.instance()
                        })
        if created:
            stock = Stock()
            stock.reservadosConfirmados = 0
            stock.reservadosNoConfirmados = cantidad
            stock.disponibles = 0
            stock.deposito = stockMinimo.deposito
            stock.producto = pVenta
            stock.save() 
        else:           
            stock, created = Stock.objects.get_or_create(producto = prod, deposito = stockMinimo.deposito, default = {
                             'reservadosConfirmados' : 0,
                             'reservadosNoConfirmados' : cantidad,
                             'disponibles' : 0,
                             'deposito' : stockMinimo.deposito,
                             'producto' : pVenta,
                             })
            if not created:
                stock.reservadosNoConfirmados = stock.reservadosNoConfirmados + cantidad
                stock.save()
        
        return stock

    def __unicode__(self):
        if self.pk == 0:
            return "NoFraccionable"
        else:
            return "Fraccionable de " + str(self.medida) + " a " + str(self.minimo)
# ===================
# = No Fraccionable =
# ===================

class NoFraccionable(Fraccionable):

    class Meta:
        proxy = True

    @classmethod
    def instance(cls):
        return NoFraccionable.objects.get(pk = ESTRATEGIA_NOFRACCIONABLE)    

    def vender(self, producto, cantidad, fraccion):
        cantidad = int(cantidad)
        stockAfectados = {}
        ventaCompleta = False
        stockMinimo = None
        stockLista = producto.stock_set.all()
        while not ventaCompleta:
            if stockLista[0].disponibles > 0:
                stockMinimo = stockLista[0]        
            for elementoLista in stockLista:
                if stockMinimo != None:
                    if (elementoLista.disponibles != 0) and (elementoLista.disponibles < stockMinimo.disponibles):
                        stockMinimo = elementoLista
                    else:
                        continue
                elif elementoLista.disponibles > 0:
                        stockMinimo = elementoLista
            if stockMinimo != None:            
                if stockMinimo.disponibles >= cantidad:
                    stockMinimo.disponibles = stockMinimo.disponibles - cantidad
                    stockMinimo.reservadosNoConfirmados = stockMinimo.reservadosNoConfirmados + cantidad
                    producto.cantidad = producto.cantidad - cantidad
                    ventaCompleta = True
                    stockMinimo.save()
                    stockAfectados[stockMinimo] = cantidad
                else:
                    stockMinimo.reservadosNoConfirmados = stockMinimo.reservadosNoConfirmados + stockMinimo.disponibles
                    cantidad = cantidad - stockMinimo.disponibles
                    stockAfectados[stockMinimo] = stockMinimo.disponibles
                    producto.cantidad = producto.cantidad - stockMinimo.disponibles
                    stockMinimo.disponibles = 0
                    stockMinimo.save()
        producto.save()                    
        return stockAfectados

    def __unicode__(self):
        return "NoFraccionable"

# =========
# = Stock =
# =========

class Stock(models.Model):
    reservadosConfirmados = models.IntegerField()
    reservadosNoConfirmados = models.IntegerField()
    disponibles = models.IntegerField()
    deposito = models.ForeignKey(Deposito, blank = True)
    producto = models.ForeignKey(Producto)
    
    def crearStock(self, disponibles, deposito, producto):
        """docstring for crearStock"""
        stock =  Stock()
        stock.reservadosConfirmados= 0
        stock.reservadosNoConfirmados= 0
        stock.producto= producto
        stock.disponibles= disponibles
        stock.deposito= deposito
        stock.save()
    
    def nuevoStock(self, disponibles, deposito, producto):
        """docstring for crearStock"""
        try:
            stock = Stock.objects.get(producto = producto, deposito = deposito)
            stock.disponibles = stock.disponibles+disponibles
            stock.save()
        except ObjectDoesNotExist:
            self.crearStock(disponibles, deposito, producto)
        
    
    def __unicode__(self):
        return "%d en deposido de %s" % (self.disponibles, self.deposito)

# ===========
# = Detalle =
# ===========

class Detalle(models.Model):

    class Meta:
        abstract = True

    cantidad = models.IntegerField()
    subtotal = models.IntegerField()
    producto = models.ForeignKey(Producto)
    deposito = models.ForeignKey(Deposito)

# ======================
# = Detalle Nota Venta =
# ======================

class DetalleNotaVenta(Detalle):
    nota = models.ForeignKey('NotaVenta')

    def setProducto(self, producto):
        self.producto = producto

    def setCantidad(self, cantidad):
        self.cantidad = cantidad
    def setSubTotal(self, subT):
        if subT > 0:
            self.subtotal = subT
        else:
            raise ErrorVenta()
    
    def setDeposito(self, deposito):
        self.deposito = deposito

    def setNota(self, notaVenta):
        self.nota = notaVenta

# ===================
# = Detalle Factura =
# ===================

class DetalleFactura(Detalle):
    factura = models.ForeignKey('Factura')
    detalleNotaVenta = models.ForeignKey(DetalleNotaVenta)

# ==============
# = Nota venta =
# ==============

class NotaVenta(models.Model):
    nombreCliente = models.CharField(max_length = 40)
    apellidoCliente = models.CharField(max_length = 20)
    fecha = models.datetime 
    precioTotal = models.IntegerField()
    facturada = models.BooleanField()
    class Meta:
        permissions = (
            ("venta", "puede vender"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )       
    
    def setNombre(self, nombre):
        if re.match('\w{3,}(\s\w+)*$', nombre):
            self.nombreCliente = nombre
        else:
            raise ErrorVenta()

    def setApellido(self, apellido):
        if re.match('\w{3,}(\s\w+)*$', apellido):
            self.apellidoCliente = apellido
        else:
            raise ErrorVenta()

    def setFecha(self, fecha):
        self.fecha = fecha

    def setPrecioTotal(self, precio):
        if precio >= 0:
            self.precioTotal = precio
        else:
            raise ErrorVenta()

    def setFacturada(self, factura):
        self.facturada = factura

# ===========
# = Factura =
# ===========

class Factura(models.Model):
    fecha = models.datetime
    formaDePago = models.CharField(max_length = 15)
    precioTotal = models.IntegerField()
    ventaNota = models.ForeignKey(NotaVenta)   

# ==========
# = Remito =
# ==========

class Remito(models.Model):
    deposito =models.ForeignKey(Deposito)
    factura =models.ForeignKey(Factura)
    entregadoCompleto = models.BooleanField()
    class Meta:
        permissions = (
            ("entregaMateriales", "puede entregar materiales"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    
    def __unicode__(self):
        return "%s" % self.pk
    
    

# ==================
# = Detalle Remito =
# ==================

class DetalleRemito(models.Model):
    cantidad = models.IntegerField()
    entregado = models.BooleanField()
    detalleFactura = models.ForeignKey(DetalleFactura)
    remito = models.ForeignKey(Remito)
    producto = models.ForeignKey(Producto)
    
# =============
# = Descuento =
# =============

class Descuento(models.Model):
    nroDescuento = models.IntegerField()
    fecha = models.datetime
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    tipoDescuento = models.ForeignKey('TipoDescuento')

# =================
# = TipoDescuento =
# =================

class TipoDescuento(Descuento):
    beneficiario = models.CharField(max_length = 40, blank = True)
    
    def __unicode__(self):
        return "%s" % self.beneficiario        