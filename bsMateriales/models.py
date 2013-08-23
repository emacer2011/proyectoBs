from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from misExcepciones import *
from datetime import *
import math
import re

# ===============
# = Clase Rubro =
# ===============

class Rubro(models.Model):
    __nombre = models.CharField(max_length = 40)
    __descripcion = models.CharField(max_length = 40, blank=True)
    
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre= nombre

    def getDescripcion(self):
        return self.__descripcion
        
    def setDescripcion(self, descripcion):
        self.__descripcion= descripcion

    def inicializar(self, nombre, descripcion, pk=None):
        self.setDescripcion(descripcion)
        self.setNombre(nombre)
        self.pk=pk

    def __unicode__(self):
        return "%s" % self.getNombre()


# ==================
# = Clase Deposito =
# ==================
class Deposito(models.Model):
    __direccion = models.CharField(max_length = 40)
    __telefono = models.CharField(max_length = 15)
    __rubro = models.ForeignKey(Rubro)
    class Meta:
        permissions = (
            ("deposito", "Abm Depositos"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    def setDireccion(self, direccion):
        if re.match('\w+(\s\w+)*$', direccion):
            self.__direccion = direccion
        else:
            raise ErrorDeposito()

    def getDireccion(self):
            return self.__direccion

    def setTelefono(self, telefono):
        if re.match('\d{7,13}$', telefono):
            self.__telefono = telefono
        else:
            raise ErrorDeposito()

    def getTelefono(self):
        return self.__telefono

    def setRubro(self, pkRubro):
        try:
            unRubro = Rubro.objects.get(pk = pkRubro)        
            self.__rubro = unRubro
        except ObjectDoesNotExist:
            raise ErrorDeposito()
    def getRubro(self):
        return self.__rubro

    def puedoEliminarlo(self): 
        try:
            stocks = Stock.objects.get(deposito = self)
            return False
        except ObjectDoesNotExist:
            return True
            
    def eliminarDeposito(self):
        print str(self.puedoEliminarlo())
        if self.puedoEliminarlo():
            self.delete()
        else:
            raise ErrorDeposito()
            
    def inicializar(self, direccion, telefono, rubro):
        self.setDireccion(direccion)
        self.setTelefono(telefono)
        self.setRubro(rubro)

    def __unicode__(self):
        return "%s" % self.getDireccion()
        
# =======================
# = Clase Tipo Producto =
# =======================
class TipoProducto(models.Model):
    __nombre = models.CharField(max_length = 40)
    __unidadMedida = models.CharField(max_length = 40)
    __descripcion = models.CharField(max_length = 40, blank=True)
    __rubro = models.ForeignKey(Rubro)    
    

    def getUnidadMedida(self):
        return __unidadMedida

    def setUnidadMedida(self, unidadMedida):
        self.__unidadMedida = unidadMedida


    def setRubro(self, pkRubro):
        try:
            unRubro = Rubro.objects.get(pk = pkRubro)        
            self.__rubro = unRubro
        except ObjectDoesNotExist:
            raise ErrorTipoProducto()
    
    def getRubro(self):
        return self.__rubro

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre= nombre

    def getDescripcion(self):
        return self.__descripcion
        
    def setDescripcion(self, descripcion):
        self.__descripcion= descripcion

    def inicializar(self, nombre, descripcion, rubro, unidadMedida, pk):
        self.setNombre(nombre)
        self.setDescripcion(descripcion)
        self.setRubro(rubro)
        self.setUnidadMedida(unidadMedida)
        self.pk = pk

    def __unicode__(self):
        return "%s" % self.getNombre()


# ====================
# = Estrategia Venta =
# ====================

ESTRATEGIA_NOFRACCIONABLE = 0

class EstrategiaVenta(models.Model):

#    class Meta:
#     abstract = True

    def vender(self, producto, cantidad, fraccion = None):
        try:
            return self.fraccionable.vender(producto, cantidad, fraccion)
        except ObjectDoesNotExist as ex:
            return self.nofraccionable.vender(producto,cantidad, fraccion)
    

    def getEstrategia(self):
        try:
            return self.fraccionable
        except ObjectDoesNotExist as ex:
            return self.nofraccionable
    

    def setMedida(self, medida):
        try:
            self.fraccionable.setMedida(medida)
        except ObjectDoesNotExist as ex:
            pass

    def setMinimo(self,minimo):
        try:
            self.nofraccionable.setMinimo(minimo)
        except ObjectDoesNotExist as ex:
            pass


    def getMedida(self):
        try:
            return self.fraccionable.getMedida()
        except ObjectDoesNotExist as ex:
            return 0

    def getMinimo(self):
        try:
            return self.fraccionable.getMinimo()
        except ObjectDoesNotExist as ex:
            return 0


# TODO: FALTA FACTORIZAR TODO ESTE CODIGO
# ==================
# = Clase Producto =
# ==================


class Producto(models.Model):
    __nombre = models.CharField(max_length = 40)
    __descripcion = models.CharField(max_length = 40, blank = True)
    __tipoProducto = models.ForeignKey(TipoProducto)
    __estrategiaVenta = models.ForeignKey(EstrategiaVenta)
    __cantidad = models.IntegerField(default= 0)
    __precio = models.FloatField()
    class Meta:
        permissions = (
            ("producto", "puede manejar abm Producto"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    
    def __unicode__(self):
        return "%s" % self.__nombre

    def puedeBorrarse(self):
        try:
            stock = Stock.objects.get(producto = self)
            return False
        except ObjectDoesNotExist:
            return True
    
    def setNombre(self,nombre):
         if re.match('\w{3,30}$', nombre):
            self.__nombre = nombre
         else:
            raise ErrorProducto()

    def getNombre(self):
         return self.__nombre
    
    def setDescripcion(self,descripcion):
         self.__descripcion = descripcion

    def getDescripcion(self):
         return self.__descripcion

    def setPrecio(self, precio):
         if precio>0:
            self.__precio = precio
         else:
            raise ErrorProducto()
            
    def getPrecio(self):
        return self.__precio

    def setCantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            raise ErrorProducto()

    def getCantidad(self):
         return self.__cantidad

    def setTipoProducto(self, tipoProducto):
        if (tipoProducto == None):
                raise ErrorProducto()
        else:
            self.__tipoProducto = tipoProducto

    def getTipoProducto(self):
        return self.__tipoProducto

    def obtenerEstrategiaDeVenta(self):
        return self.__estrategiaVenta.getEstrategia()        
    
    def esFraccionable(self):
        if self.__estrategiaVenta.pk == ESTRATEGIA_NOFRACCIONABLE:
            return False     
        return True

    def setEstrategiaDeVenta(self, estrategiaVenta):
        self.__estrategiaVenta= estrategiaVenta

    def verificarCantidadStock(self):
        stockList = self.stock_set.all()
        cantidad = 0
        for stock in stockList:
            cantidad += stock.getDisponibles()
        return cantidad            

    def vender(self, cantidad = None, fraccion = 5):
        if (int(cantidad) <= 0) or (int(cantidad) > self.verificarCantidadStock()):
            raise ErrorVenta()
        else:
            return self.obtenerEstrategiaDeVenta().vender(self, cantidad, fraccion)
        
    def inicializar(self, nombre, descripcion, tipoProducto, precio, estrategiaVenta):
        self.setNombre(nombre)
        self.setDescripcion(descripcion)
        self.setTipoProducto(tipoProducto)
        self.setPrecio(precio)
        self.setEstrategiaDeVenta(estrategiaVenta) 

# ===================
# = No Fraccionable =
# ===================

class NoFraccionable(EstrategiaVenta):

    @classmethod
    def instance(cls):
        return NoFraccionable.objects.get(pk = ESTRATEGIA_NOFRACCIONABLE)    

    
    def stocksAfectados (self, producto, cantidad):
        listaStocks = []
        #Caso en que un solo deposito cumple con la totalidad de la demanda
        stocksOrdenados = sorted(producto.stock_set.all(), key=lambda stock: stock.disponibles)
        for stock in stocksOrdenados:
            if stock.disponibles >= cantidad:
                return [stock]
        stocksOrdenados = sorted(producto.stock_set.all(), key=lambda stock: stock.disponibles, reverse=True)
        #Caso contrario
        for stock in stocksOrdenados:
            listaStocks.append(stock)
            cantidad = cantidad - stock.disponibles
            if cantidad <= 0:   
                return listaStocks

    def vender(self, producto, cantidad, fraccion = None):

        cantidad = int(cantidad)
        depositosAfectados = {}
        if producto.verificarCantidadStock() >= cantidad:
            stocks = self.stocksAfectados(producto, cantidad)

            producto.setCantidad(producto.getCantidad() - cantidad)
            producto.save()
            for stock in stocks:
                if cantidad > 0:
                    if stock.disponibles >= cantidad:
                        stock.disponibles = stock.disponibles - cantidad
                        stock.reservadosNoConfirmados = stock.reservadosNoConfirmados + cantidad
                        stock.save()
                        depositosAfectados[stock] = cantidad
                        cantidad = 0
                        return depositosAfectados
                    else:
                        cantidad = cantidad - stock.disponibles
                        stock.reservadosNoConfirmados = stock.reservadosNoConfirmados + stock.disponibles
                        cantidadTemporal= stock.disponibles
                        stock.disponibles = 0
                        stock.save()
                        depositosAfectados[stock]= cantidadTemporal 
            return depositosAfectados
        else:
            raise ErrorVenta()


# =================
# = Fraccionables =
# =================

class Fraccionable(EstrategiaVenta):
    __medida = models.FloatField() # TODO: medidas a float
    __minimo = models.FloatField()


    def setMedida(self, medida):
        if medida > 0:
            self.__medida = medida
        else:
            raise ErrorProducto()

    def setMinimo(self,minimo):
        if minimo > 0:
            self.__minimo = minimo
        else:
            raise ErrorProducto()


    def getMedida(self):
        return self.__medida

    def getMinimo(self):
        return self.__minimo

    def vender(self, producto, cantidad, fraccion):
        stockLista = producto.stock_set.all()
        stockMinimo = None
        stockAfectados = {}
        ventaCompleta = False

        if ((fraccion > self.getMedida() )or(fraccion< self.getMinimo())):
            raise ErrorProducto 

    # Llamar funcion que diga exactamente cuanto restar y crea los productos necesarios!
        can 
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

    def fraccionar(self, producto, fraccion, cantidad):
        cantidadXunidad = math.floor(self.getMedida()/fraccion)
        resto =(self.getMedida() % fraccion)
        if ((resto<self.getMinimo()) and (resto != 0)):
            cantidadXunidad = cantidadXunidad -1
        cantidadAfectada = math.floor(cantidad / cantidadXunidad)
        if (cantidad % cantidadXunidad) > 0:
            cantidadAfectada = cantidadAfectada+1

        return cantidadAfectada


# =========
# = Stock =
# =========

class Stock(models.Model):
    reservadosConfirmados = models.IntegerField()
    reservadosNoConfirmados = models.IntegerField()
    disponibles = models.IntegerField()
    deposito = models.ForeignKey(Deposito, blank = True)
    producto = models.ForeignKey(Producto)

    def getReservadoConfirmados(self):
        return self.reservadosConfirmados

    def getReservadoNoconfirmados(self):
        return self.reservadosNoConfirmados

    def setReservadoConfirmados(self, reservadosConfirmados):
        self.reservadosConfirmados = reservadosConfirmados

    def setReservadoNoconfirmados(self, reservadosNoConfirmados):
        self.reservadosNoConfirmados = reservadosNoConfirmados

    def getDisponibles(self):
        return self.disponibles
    
    def setDisponibles(self, disponible):
        if disponible < 0:
            raise ErrorStock()
        else:
            self.disponibles = disponible

    def getDeposito(self):
        return self.deposito

    def setDeposito(self, deposito):
        self.deposito = deposito

    def getProducto(self):
        return self.producto

    def setProducto(self, producto):
        self.producto = producto

    @classmethod
    def cargarStock(cls, disponibles, deposito, producto):
        """docstring for crearStock"""
        if disponibles <= 0:
            raise ErrorStock()
        else:
            stock, created = Stock.objects.get_or_create(producto = producto, deposito = deposito, defaults = {
                             'reservadosConfirmados' : 0,
                             'reservadosNoConfirmados' : 0,
                             'producto' : producto,
                             'disponibles' : disponibles,
                             'deposito' : deposito
                             })
            if not created:
                stock.setDisponibles(stock.getDisponibles() + disponibles)
                stock.save()
    
    def __unicode__(self):
        return "%d en deposido: %s" % (self.getDisponibles(), self.getDeposito())

# ===========
# = Detalle =
# ===========

class Detalle(models.Model):

    class Meta:
        abstract = True

    cantidad = models.IntegerField()
    subtotal = models.FloatField()
    producto = models.ForeignKey(Producto)


    def getCantidad(self):
        return self.cantidad

    def setCantidad(self, cantidad):
        if cantidad>=0:
            self.cantidad = cantidad
        else:
            raise ErrorVenta()

    def getSubTotal(self):
        return self.subtotal

    def setSubTotal(self, subT):
        if subT > 0:
            self.subtotal = subT
        else:
            raise ErrorVenta()
    
    def getProducto(self):
        return self.producto

    def setProducto(self, producto):
        self.producto = producto

    

# ======================
# = Detalle Nota Venta =
# ======================

class DetalleNotaVenta(Detalle):
    nota = models.ForeignKey('NotaVenta')
    deposito = models.ForeignKey(Deposito)

    def setNota(self, notaVenta):
        self.nota = notaVenta

    def getNota(self):
        return self.nota

    def setDeposito(self, deposito):
        self.deposito = deposito
    
    def getDeposito(self):
        return self.deposito

    def inicializar(self, producto, cantidad, subTotal, deposito, notaVenta):
        self.setProducto(producto)
        self.setCantidad(cantidad)
        self.setSubTotal(subTotal)
        self.setDeposito(deposito)
        self.setNota(notaVenta)
        


# ===================
# = Detalle Factura =
# ===================

class DetalleFactura(Detalle):
    factura = models.ForeignKey('Factura')
    detalleNotaVenta = models.ForeignKey(DetalleNotaVenta)

    def getDetalleNotaVenta(self):
        return self.detalleNotaVenta

    def setDetalleNotaVenta(self, detalle):
        self.detalleNotaVenta = detalle

    def getFactura(self):
        return self.factura

    def setFactura(self, factura):
        self.factura = factura

    def inicializar(self, detalle, factura, producto, cantidad, subTotal):
        self.setDetalleNotaVenta(detalle)
        self.setFactura(factura)
        self.setProducto(producto)
        self.setCantidad(cantidad)
        self.setSubTotal(subTotal)


# ==============
# = Nota venta =
# ==============

class NotaVenta(models.Model):
    nombreCliente = models.CharField(max_length = 40)
    apellidoCliente = models.CharField(max_length = 20)
    fecha = models.datetime
    precioTotal = models.IntegerField(default=0)
    facturada = models.BooleanField(default=False)
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

    def getNombre(self):
        return self.nombreCliente

    def setApellido(self, apellido):
        if re.match('\w{3,}(\s\w+)*$', apellido):
            self.apellidoCliente = apellido
        else:
            raise ErrorVenta()

    def getApellido(self):
        return self.apellidoCliente

    def setFecha(self, fecha):
        self.fecha = fecha

    def getFecha(self):
        return self.fecha

    def getPrecioTotal(self):
        return self.precioTotal
    
    def setPrecioTotal(self, precio):
        if precio >= 0:
            self.precioTotal = precio
        else:
            raise ErrorVenta()

    def incrementarTotal(self, cantidad):
        self.precioTotal += cantidad

    def setFacturada(self, factura):
        self.facturada = factura

    def getFacturada(self):
        return self.facturada

    def inicializar(self, nombrePersona= None, apellidoPersona= None):
        self.setNombre(nombrePersona)
        self.setApellido(apellidoPersona)
        self.setFecha(date.today())

        


# ===========
# = Factura =
# ===========

class Factura(models.Model):
    fecha = models.datetime
    formaDePago = models.CharField(max_length = 15)
    precioTotal = models.FloatField()
    ventaNota = models.ForeignKey(NotaVenta)

    def getFecha(self):
        return self.fecha
    
    def setFecha(self, fecha):
        self.fecha = fecha

    def getFormaDePago(self):
        return self.formaDePago

    def setFormaDePago(self, formaDePago):
        self.formaDePago = formaDePago

    def getPrecioTotal(self):
        return self.precioTotal

    def setPrecioTotal(self, precioTotal):
        self.precioTotal = precioTotal

    def getVentaNota(self):
        return self.ventaNota

    def setVentaNota(self, ventaNota):
        self.ventaNota = ventaNota

    def inicializar(self, formaDePago, precioTotal, ventaNota): 
        self.setFormaDePago(formaDePago)
        self.setPrecioTotal(precioTotal)
        self.setVentaNota(ventaNota)
        self.setFecha(date.today())


# ==========
# = Remito =
# ==========

class Remito(models.Model):
    deposito =models.ForeignKey(Deposito)
    factura =models.ForeignKey(Factura)
    entregadoCompleto = models.BooleanField(default = False)
    class Meta:
        permissions = (
            ("entregaMateriales", "puede entregar materiales"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    
    def actualizarEntregados(self):
        entregado = True
        detalles = DetalleRemito.objects.filter(remito = self.pk)
        for detalle in detalles:
            entregado = entregado & detalle.entregado
        self.entregadoCompleto = entregado
        self.save()
    
    def getDeposito(self):
        return self.deposito

    def setDeposito(self, deposito):
        self.deposito = deposito

    def getFactura(self):
        return self.factura

    def setFactura(self, factura):
        self.factura = factura

    def setEntregadoCompleto(self, valor):
        self.entregadoCompleto = valor
    
    def getEntregadoCompleto(self):
        return self.entregadoCompleto

    def inicializar(self, factura, deposito):
        self.setFactura(factura)
        self.setDeposito(deposito)


# ==================
# = Detalle Remito =
# ==================

class DetalleRemito(models.Model):
    cantidad = models.IntegerField()
    entregado = models.BooleanField(default = False)
    detalleFactura = models.ForeignKey(DetalleFactura)
    remito = models.ForeignKey(Remito)
    producto = models.ForeignKey(Producto)

    def setCantidad(self, cantidad):
        self.cantidad = cantidad

    def getCantidad(self):
        return self.cantidad

    def setEntregado(self, entregado):
        self.entregado = entregado

    def getEntregado(self):
        return self.entregado
    
    def setDetalleFactura(self, detalle):
        self.detalleFactura = detalle

    def getDetalleFactura(self):
        return self.detalleFactura

    def setRemito(self, remito):
        self.remito = remito

    def getRemito(self):
        return self.remito

    def setProducto(self, producto):
        self.producto = producto
    
    def getProducto(self):
        return self.producto

    def confirmarStock(self):
        """docstring for confirmarStock"""
        stock = Stock.objects.get(producto = self.producto, deposito= self.remito.deposito)
        if self.entregado:
                stock.reservadosConfirmados= int(stock.reservadosConfirmados)-int(self.cantidad)
        else: 
              stock.reservadosConfirmados= int(stock.reservadosConfirmados)+int(self.cantidad)
        stock.save()

    def inicializar(self, cantidad, detalle, remito, producto):
        self.setCantidad(cantidad)
        self.setDetalleFactura(detalle)
        self.setRemito(remito)
        self.setProducto(producto)
        
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
