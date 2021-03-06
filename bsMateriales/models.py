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
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank=True)
    
    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre= nombre

    def getDescripcion(self):
        return self.descripcion
        
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion

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
    direccion = models.CharField(max_length = 40)
    telefono = models.CharField(max_length = 15)
    rubro = models.ForeignKey(Rubro)
    class Meta:
        permissions = (
            ("deposito", "puede manejar abm Deposito"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    def setDireccion(self, direccion):
        if re.match('\w+(\s\w+)*$', direccion):
            self.direccion = direccion
        else:
            raise ErrorDeposito()

    def getDireccion(self):
            return self.direccion

    def setTelefono(self, telefono):
        if re.match('\d{7,13}$', telefono):
            self.telefono = telefono
        else:
            raise ErrorDeposito()

    def getTelefono(self):
        return self.telefono

    def setRubro(self, pkRubro):
        try:
            unRubro = Rubro.objects.get(pk = pkRubro)        
            self.rubro = unRubro
        except ObjectDoesNotExist:
            raise ErrorDeposito()
    def getRubro(self):
        return self.rubro

    def limpiarStockVacio(self):
        stocks = Stock.objects.filter(deposito = self)
        for stock in stocks:
            if ((stock.getDisponibles() == 0) and (stock.getReservadoNoConfirmados() == 0) and (stock.getReservadoConfirmados() == 0)):
                stock.delete()

    def puedoEliminarlo(self):
        self.limpiarStockVacio() 
        stocks = Stock.objects.filter(deposito = self)
        if (stocks.count() != 0):
            for stock in stocks:
                if (stock.getDisponibles() == 0) and (stock.getReservadoConfirmados() == 0) and (stock.getReservadoNoConfirmados() == 0):
                    return True
            return False
        else:
            return True
            
    def eliminarDeposito(self):
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
    nombre = models.CharField(max_length = 40)
    unidadMedida = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank=True)
    rubro = models.ForeignKey(Rubro)    
    

    def getUnidadMedida(self):
        return unidadMedida

    def setUnidadMedida(self, unidadMedida):
        self.unidadMedida = unidadMedida


    def setRubro(self, pkRubro):
        try:
            unRubro = Rubro.objects.get(pk = pkRubro)        
            self.rubro = unRubro
        except ObjectDoesNotExist:
            raise ErrorTipoProducto()
    
    def getRubro(self):
        return self.rubro

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre= nombre

    def getDescripcion(self):
        return self.descripcion
        
    def setDescripcion(self, descripcion):
        self.descripcion= descripcion

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
    medida = models.FloatField(default=0.0) # TODO: medidas a float
    
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
            self.nofraccionable.setMinimo(minimo)#TODO: revisar!
        except ObjectDoesNotExist as ex:
            pass


    def getMedida(self):
        try:
            return self.fraccionable.getMedida()
        except ObjectDoesNotExist as ex:
            return self.nofraccionable.getMedida()

    def getMinimo(self):
        try:
            return self.fraccionable.getMinimo()
        except ObjectDoesNotExist as ex:
            return '-'

    def verificarCantidadStock(self, producto, fraccion = None):
        try:
            return self.fraccionable.verificarCantidadStock(producto,fraccion)
        except ObjectDoesNotExist as ex:
            return self.nofraccionable.verificarCantidadStock(producto,fraccion)

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


# TODO: FALTA FACTORIZAR TODO ESTE CODIGO
# ==================
# = Clase Producto =
# ==================


class Producto(models.Model):
    nombre = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 40, blank = True)
    tipoProducto = models.ForeignKey(TipoProducto)
    estrategiaVenta = models.ForeignKey(EstrategiaVenta)
    cantidad = models.IntegerField(default= 0)
    precio = models.FloatField()
    class Meta:
        permissions = (
            ("producto", "puede manejar abm Producto"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
    
    def __unicode__(self):
        return "%s" % self.nombre

    def puedeBorrarse(self):
        try:
            self.limpiarStock()
            stock = Stock.objects.get(producto = self)
            return False
        except ObjectDoesNotExist:
            return True
    
    def setNombre(self,nombre):
         if re.match('\w{3,30}$', nombre):
            self.nombre = nombre
         else:
            raise ErrorProducto()

    def getNombre(self):
         return self.nombre
    
    def setDescripcion(self,descripcion):
         self.descripcion = descripcion

    def getDescripcion(self):
         return self.descripcion

    def setPrecio(self, precio):
         if precio>0:
            self.precio = precio
         else:
            raise ErrorProducto()
            
    def getPrecio(self):
        return self.precio

    def setCantidad(self, cantidad):
        if cantidad >= 0:
            self.cantidad = cantidad
        else:
            raise ErrorProducto()

    def getCantidad(self):
         return self.cantidad

    def setTipoProducto(self, tipoProducto):
        if (tipoProducto == None):
                raise ErrorProducto()
        else:
            self.tipoProducto = tipoProducto

    def getTipoProducto(self):
        return self.tipoProducto

    def obtenerEstrategiaDeVenta(self):
        return self.estrategiaVenta.getEstrategia()        
    
    def esFraccionable(self):
        if self.estrategiaVenta.pk == ESTRATEGIA_NOFRACCIONABLE:
            return False     
        return True

    def setEstrategiaDeVenta(self, estrategiaVenta):
        self.estrategiaVenta= estrategiaVenta

    def limpiarStock(self):
        stocks = Stock.objects.filter(producto = self)
        for stock in stocks:
            if ((stock.getDisponibles() == 0) and (stock.getReservadoNoConfirmados() == 0) and (stock.getReservadoConfirmados() == 0)):
                stock.delete()
        return

    def vender(self, cantidad = None, fraccion = None):
        if (int(cantidad) <= 0) or (int(cantidad) > self.obtenerEstrategiaDeVenta().verificarCantidadStock(self, fraccion)):
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


    def setMedida(self,medida):
        if medida > 0:
            self.medida = medida
        else:
            raise ErrorProducto()

    def getMedida(self):
        if  self.medida == 0.0:
            return '-'
        return self.medida

    def verificarCantidadStock(self, producto, fraccion = None):
        return producto.getCantidad()

    def vender(self, producto, cantidad, fraccion = None):

        cantidad = int(cantidad)
        depositosAfectados = {}
        if self.verificarCantidadStock(producto) >= cantidad:
            stocks = self.stocksAfectados(producto, cantidad)

            producto.setCantidad(producto.getCantidad() - cantidad)
            producto.save()
            for stock in stocks:
                if cantidad > 0:
                    if stock.getDisponibles() >= cantidad:
                        stock.setDisponibles(stock.getDisponibles() - cantidad)
                        stock.setReservadoNoConfirmados(stock.getReservadoNoConfirmados() + cantidad)
                        stock.save()
                        depositosAfectados[stock] = (cantidad, producto, producto.obtenerEstrategiaDeVenta().getMedida())
                        cantidad = 0
                        return depositosAfectados
                    else:
                        cantidad = cantidad - stock.disponibles
                        stock.setReservadoNoConfirmados(stock.getReservadoNoConfirmados() + stock.getDisponibles())
                        cantidadTemporal= stock.getDisponibles()
                        stock.setDisponibles(0)
                        stock.save()
                        depositosAfectados[stock]= (cantidadTemporal, producto, producto.obtenerEstrategiaDeVenta().getMedida())
            return depositosAfectados
        else:
            raise ErrorVenta()


# =================
# = Fraccionables =
# =================

class Fraccionable(EstrategiaVenta):
    minimo = models.FloatField()


    def setMedida(self, medida):
        if medida > 0:
            self.medida = medida
        else:
            raise ErrorProducto()

    def getMedida(self):
        return self.medida

    def setMinimo(self,minimo):
        if minimo > 0:
            self.minimo = minimo
        else:
            raise ErrorProducto()

    def getMinimo(self):
        return self.minimo

    def verificarCantidadStock(self, producto, fraccion):
        fraccion = float(fraccion)
        cantidadXunidad = math.floor(self.getMedida()/fraccion)
        resto =(self.getMedida() % fraccion)
        if ((resto<self.getMinimo()) and (resto != 0)):
            cantidadXunidad = cantidadXunidad -1
        cantidad = cantidadXunidad * producto.getCantidad()
        return cantidad            

    def vender(self, producto, cantidad, fraccion):
        depositosAfectados = {}        
        cantidad = int(cantidad)
        fraccion = float(fraccion)

        if ((fraccion > self.getMedida()) or (fraccion< self.getMinimo())):
            raise ErrorProducto 
        medidas = self.fraccionar(fraccion, cantidad)
        productosAfectados = medidas['productosMaximaFraccion'] + medidas['productoMinimaFraccion']
        listaStocks = self.stocksAfectados(producto, productosAfectados)
        if (medidas['productosMaximaFraccion'] != 0):
            depositosAfectados = self.realizarVenta(depositosAfectados, producto, listaStocks, medidas['productosMaximaFraccion'],medidas['cantidadXunidad'], fraccion)
        if (medidas['productoMinimaFraccion'] != 0):
            depositosAfectados = self.realizarVenta(depositosAfectados, producto, listaStocks, 1,medidas['productoMinimaFraccion'], fraccion)
        return  depositosAfectados


    def realizarVenta(self, depositosAfectados, producto, stocks, cantidadProductos, cantidadXunidad, fraccion):
        cantidad = cantidadProductos
        for stock in stocks:
            if cantidad > 0:
                if (stock.getDisponibles() >= cantidad):
                    stock.setDisponibles(stock.getDisponibles() - cantidad)
                    stock.save()
                    if depositosAfectados.has_key(stock):
                        depositosAfectados[stock] = (cantidad * cantidadXunidad,None,producto.obtenerEstrategiaDeVenta().getMedida())
                    else:
                        depositosAfectados[stock] = (cantidad * cantidadXunidad, None,producto.obtenerEstrategiaDeVenta().getMedida())
                    cantidad = 0
                else:
                    cantidad -= stock.disponibles
                    cantidadTemporal = stock.getDisponibles()
                    stock.setDisponibles(0)
                    stock.save()
                    if depositosAfectados.has_key(stock):
                        depositosAfectados[stock] = (cantidadTemporal * cantidadXunidad,None,producto.obtenerEstrategiaDeVenta().getMedida())
                    else:
                        depositosAfectados[stock] = (cantidadTemporal * cantidadXunidad,None,producto.obtenerEstrategiaDeVenta().getMedida())
            else:
                break
        producto.setCantidad(producto.getCantidad() - cantidadProductos)
        producto.save()
        self.generarProductoNuevo(depositosAfectados, cantidadXunidad, fraccion, producto, cantidadProductos)
        return self.generarProductoVendido(depositosAfectados, fraccion, producto)

    def generarProductoNuevo(self, depositosAfectados, cantidadXunidad, fraccion, producto, cantidadProductos):
        medidaNueva = self.getMedida() - (cantidadXunidad * fraccion)
        if (medidaNueva != 0):
        
            if (medidaNueva > self.getMinimo()):
                estrategia = Fraccionable()
                estrategia.setMedida(medidaNueva)
                estrategia.setMinimo(self.getMinimo())
                estrategia.save()
            else:
                estrategia = NoFraccionable()
                estrategia.setMedida(medidaNueva)
                estrategia.save()
            """
            CONSULTA PARA BUSCAR SI YA EXISTE EL NUEVO PRODUCTO
            """

            if (isinstance(estrategia,Fraccionable)):
                qs = Producto.objects.filter(nombre=producto.getNombre(),estrategiaVenta__fraccionable__medida=medidaNueva)
            else:
                qs = Producto.objects.filter(nombre=producto.getNombre(),estrategiaVenta__nofraccionable__isnull=False)
          
            if (qs.count() != 0):
                productoExistente = qs[0]
                stocks = depositosAfectados.keys()
                for stock in stocks:
                    """
                    VERIFICO SI EL PRODUCTO EXISTENTE TIENE STOCK EN EL MISMO DEPOSITO
                    qs1 = Stock.objects.filter(deposito__direccion = stock.getDeposito().getDireccion(),producto__nombre=producto.getNombre(),producto__estrategiaVenta__fraccionable__medida=medidaNueva)                    """
                 #   qs1 = Stock.objects.filter(deposito__direccion = stock.getDeposito().getDireccion(),producto__nombre=productoExistente.getNombre(),producto__estrategiaVenta__fraccionable__medida=medidaNueva)
                    qs1 = Stock.objects.filter(deposito= stock.getDeposito(),producto=productoExistente)
                    if (qs1.count() != 0):
                        stockExistente = qs1[0] # no estara generando uno nuevo aca =
                        stockExistente.setDisponibles(stockExistente.getDisponibles() + cantidadProductos)
                        stockExistente.save()
                    else:
                        stockNuevo = Stock()
                        stockNuevo.setReservadoNoConfirmados(0)
                        stockNuevo.setReservadoConfirmados(0)
                        stockNuevo.setDisponibles(cantidadProductos)
                        stockNuevo.setDeposito(stock.getDeposito())
                        stockNuevo.setProducto(productoExistente)
                        stockNuevo.save()    
                
                productoExistente.setCantidad(productoExistente.getCantidad() + cantidadProductos)
                productoExistente.save()
            else:
                productoNuevo = Producto()
                productoNuevo.setNombre(producto.getNombre())
                productoNuevo.setDescripcion(producto.getNombre() + " de " + str(medidaNueva))
                productoNuevo.setTipoProducto(producto.getTipoProducto())
                productoNuevo.setPrecio(producto.getPrecio())
                productoNuevo.setCantidad(cantidadProductos)
                productoNuevo.setEstrategiaDeVenta(estrategia)
                productoNuevo.save()

                stocks = depositosAfectados.keys()
                for stock in stocks:
                    stockNuevo = Stock()
                    stockNuevo.setReservadoNoConfirmados(0)
                    stockNuevo.setReservadoConfirmados(0)
                    stockNuevo.setDisponibles(cantidadProductos)
                    stockNuevo.setDeposito(stock.getDeposito())
                    stockNuevo.setProducto(productoNuevo)
                    stockNuevo.save()
        return

    def generarProductoVendido(self, depositosAfectados, fraccion, producto):
        if (fraccion > self.getMinimo()):
            estrategia = Fraccionable()
            estrategia.setMedida(fraccion)
            estrategia.setMinimo(self.getMinimo())
            estrategia.save()
        else:
            estrategia = NoFraccionable()
            estrategia.setMedida(fraccion)
            estrategia.save()
        """
        CONSULTA PARA BUSCAR SI YA EXISTE EL PRODUCTO QUE SE GENERO AL VENDER
        """
        if (isinstance(estrategia,Fraccionable)):
            qs = Producto.objects.filter(nombre=producto.getNombre(),estrategiaVenta__fraccionable__medida=fraccion)
        else:
            qs = Producto.objects.filter(nombre=producto.getNombre(),estrategiaVenta__nofraccionable__isnull=False)
        if (qs.count() != 0):
            productoExistente = qs[0]
            stocks = depositosAfectados.keys()
            for stock in stocks:
                """
                VERIFICO SI EL PRODUCTO EXISTENTE TIENE STOCK EN EL MISMO DEPOSITO
                """
                qs1 = Stock.objects.filter(deposito = stock.getDeposito(),producto=productoExistente)
                if (qs1.count() != 0):
                    stockExistente = qs1[0]
                    stockExistente.setReservadoNoConfirmados(stockExistente.getReservadoNoConfirmados() + depositosAfectados[stock][0])
                    stockExistente.save()
                else:
                    stockNuevo = Stock()
                    stockNuevo.setReservadoNoConfirmados(depositosAfectados[stock][0])
                    stockNuevo.setReservadoConfirmados(0)
                    stockNuevo.setDisponibles(0)
                    stockNuevo.setDeposito(stock.getDeposito())
                    stockNuevo.setProducto(productoExistente)
                    stockNuevo.save()
                depositosAfectados[stock] = (depositosAfectados[stock][0], productoExistente,producto.obtenerEstrategiaDeVenta().getMedida())
            productoExistente.save()
        else:
            productoNuevo = Producto()
            productoNuevo.setNombre(producto.getNombre())
            productoNuevo.setDescripcion(producto.getNombre() + " de " + str(fraccion))
            productoNuevo.setTipoProducto(producto.getTipoProducto())
            productoNuevo.setPrecio(producto.getPrecio())
            productoNuevo.setCantidad(0)
            productoNuevo.setEstrategiaDeVenta(estrategia)
            productoNuevo.save()

            stocks = depositosAfectados.keys()
            for stock in stocks:
                stockNuevo = Stock()
                stockNuevo.setReservadoNoConfirmados(depositosAfectados[stock][0])
                stockNuevo.setReservadoConfirmados(0)
                stockNuevo.setDisponibles(0)
                stockNuevo.setDeposito(stock.getDeposito())
                stockNuevo.setProducto(productoNuevo)
                stockNuevo.save()
                depositosAfectados[stock] = (depositosAfectados[stock][0], productoNuevo,producto.obtenerEstrategiaDeVenta().getMedida())
        return depositosAfectados
        

    def fraccionar(self, fraccion, cantidad):
        valoresDeMedidas = {}
        cantidadXunidad = math.floor(self.getMedida()/fraccion)
        resto =(self.getMedida() % fraccion)
        if ((resto<self.getMinimo()) and (resto != 0)):
            cantidadXunidad = cantidadXunidad -1
        valoresDeMedidas['productosMaximaFraccion'] = math.floor(cantidad / cantidadXunidad)
        valoresDeMedidas['cantidadXunidad'] = cantidadXunidad
        valoresDeMedidas['productoMinimaFraccion'] = cantidad % cantidadXunidad
        return valoresDeMedidas


# =========
# = Stock =
# =========

class Stock(models.Model):
    reservadosConfirmados = models.IntegerField()
    reservadosNoConfirmados = models.IntegerField()
    disponibles = models.IntegerField()
    deposito = models.ForeignKey(Deposito, blank = True)
    producto = models.ForeignKey(Producto)

    class Meta:
        permissions = (
            ("stock", "puede cargar/eliminar stock"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )

    def getReservadoConfirmados(self):
        return self.reservadosConfirmados

    def getReservadoNoConfirmados(self):
        return self.reservadosNoConfirmados

    def setReservadoConfirmados(self, reservadosConfirmados):
        self.reservadosConfirmados = reservadosConfirmados

    def setReservadoNoConfirmados(self, reservadosNoConfirmados):
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
        return "%d en deposito: %s" % (self.getDisponibles(), self.getDeposito())
    
    def __cmp__(self,other):
        if self.producto.pk > other.producto.pk:
            return 1
        if self.producto.pk < other.producto.pk:
            return -1 
        return 0
# ===========
# = Detalle =
# ===========

class Detalle(models.Model):

    class Meta:
        abstract = True

    cantidad = models.IntegerField()
    subtotal = models.FloatField()
    producto = models.ForeignKey(Producto)
    medidaOrigen = models.CharField(max_length = 11)


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

    def inicializar(self, producto, cantidad, subTotal, deposito, notaVenta, medidaOrigen):
        self.setProducto(producto)
        self.setCantidad(cantidad)
        self.setSubTotal(subTotal)
        self.setDeposito(deposito)
        self.setNota(notaVenta)
        self.medidaOrigen = medidaOrigen
        


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

    def inicializar(self, detalle, factura, producto, cantidad, subTotal, medidaOrigen):
        self.setDetalleNotaVenta(detalle)
        self.setFactura(factura)
        self.setProducto(producto)
        self.setCantidad(cantidad)
        self.setSubTotal(subTotal)
        self.medidaOrigen = medidaOrigen


# ==============
# = Nota venta =
# ==============

class NotaVenta(models.Model):
    nombreCliente = models.CharField(max_length = 40)
    apellidoCliente = models.CharField(max_length = 20)
    fecha = models.CharField(max_length = 11)
    precioTotal = models.FloatField(default = 0)
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
        self.setFecha(date.today().__str__())

        


# ===========
# = Factura =
# ===========

class Factura(models.Model):
    fecha = models.CharField(max_length = 11)
    formaDePago = models.CharField(max_length = 15)
    precioTotal = models.FloatField()
    ventaNota = models.ForeignKey(NotaVenta)


    class Meta:
        permissions = (
            ("cobrar", "puede cobrar"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )


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
        self.setFecha(date.today().__str__())



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
    medidaOrigen = models.CharField(max_length = 11)

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
                stock.setReservadoConfirmados(int(stock.getReservadoConfirmados()) - int(self.cantidad))
        else: 
              stock.setReservadoConfirmados(int(stock.getReservadoConfirmados()) + int(self.cantidad))
        stock.save()

    def inicializar(self, cantidad, detalle, remito, producto, medidaOrigen):
        self.setCantidad(cantidad)
        self.setDetalleFactura(detalle)
        self.setRemito(remito)
        self.setProducto(producto)
        self.medidaOrigen = medidaOrigen
        
# =============
# = Descuento =
# =============

class Descuento(models.Model):
    fecha = models.datetime
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    deposito = models.ForeignKey(Deposito)
    descripcion = models.CharField(max_length = 100, blank = True)
    tipoDescuento = models.ForeignKey('TipoDescuento')

    def getFecha(self):
        return self.fecha

    def setFecha(self, fecha):
        self.fecha = fecha

    def getCantidad(self):
        return self.cantidad

    def setCantidad(self, cantidad):
        if (int(cantidad) > 0) and (self.producto.getCantidad() >= cantidad):
            self.cantidad = cantidad
        else:
            raise ErrorDescuento()

    def getProducto(self):
        return self.producto

    def setProducto(self, producto):
        self.producto = producto

    def getDeposito(self):
        return self.deposito 

    def setDeposito(self, deposito):
        self.deposito = deposito

    def getDescripcion(self):
        return self.descripcion

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def getTipoDescruento(self):
        return  self.tipoDescuento

    def setTipoDescuento(self, tipo, beneficiario = None):
        if (tipo == "Donacion"):
            tipoDescuento = TipoDescuento()
            tipoDescuento.setNombre(tipo)
            tipoDescuento.setBeneficiario(beneficiario)
            tipoDescuento.save()
            self.tipoDescuento = tipoDescuento
        else:
            descuento, created = TipoDescuento.objects.get_or_create(nombre = tipo, defaults = {'nombre' : tipo})
            descuento.save()
            self.tipoDescuento = descuento
             
    def descontarStock(self):
        try:
            stock = Stock.objects.get(deposito = self.deposito, producto = self.producto)
            stock.setDisponibles(stock.getDisponibles() - self.cantidad)
            self.getProducto().setCantidad(self.getProducto().getCantidad() - self.cantidad)
            stock.save()
            self.getProducto().limpiarStock()
            self.getProducto().save()
        except ObjectDoesNotExist:
            raise ErrorDescuento() 

    def inicializar(self, cantidad, producto, deposito, descripcion, tipoDescuento, beneficiario = None):
        self.setProducto(producto)
        self.setDeposito(deposito)
        self.setCantidad(cantidad)
        self.setDescripcion(descripcion)
        self.setTipoDescuento(tipoDescuento,beneficiario)


# =================
# = TipoDescuento =
# =================

class TipoDescuento(models.Model):
    nombre = models.CharField(max_length = 40)
    beneficiario = models.CharField(max_length = 40, blank = True)

    def setNombre(self, nombre):
        self.nombre = nombre

    def setBeneficiario(self, beneficiario):
        self.beneficiario = beneficiario
    
    def __unicode__(self):
        return "%s" % self.nombre       
