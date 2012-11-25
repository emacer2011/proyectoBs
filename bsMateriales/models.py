from django.db import models
from django.core.exceptions import ObjectDoesNotExist
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
            return NoFraccionable.intance()
        return self.estrategiaVenta

    def vender(self, cantidad = None, fraccion = None):
        return self.obtenerEstrategiaDeVenta().vender(self, cantidad = cantidad, fraccion = fraccion)
        
# ====================
# = Estrategia Venta =
# ====================

ESTRATEGIA_NOFRACCIONABLE = 0

class EstrategiaVenta(models.Model):

    class Meta:
        abstract = True

    def vender(self, producto, cantidad, fraccion):
        raise NotImplemented    
# =================
# = Fraccionables =
# =================

class Fraccionable(EstrategiaVenta):
    medida = models.IntegerField()
    minimo = models.IntegerField()

    def vender(self, producto, cantiad = None, fraccion = None):
        stockLista = producto.stock_set.all()
        stockLista[0].disponibles = stockLista[0].disponibles - 1
#        producto = self.fraccionar(producto, fraccion)
#        producto.save()

#    def fraccionar(self, producto, cantiad, fraccion):
        pSobra = Producto()
        pSobra.nombre = producto.nombre
        pSobra.descripcion = "producto nuevo generado para stock"
        pSobra.tipoProductoConcreto = producto.tipoProductoConcreto

        resto = self.medida - fraccion
        if resto > self.minimo:
          	pSobra.estrategiaVenta = Fraccionable(medida = resto, minimo = self.minimo)
        else:
          	pSobra.estrategiaVenta = NoFraccionable()

        stock = Stock()
        stock.reservadosConfirmados = 0
        stock.reservadosNoConfirmados = 0
        stock.disponibles = 1
        stock.deposito = stockLista[0].deposito
        stock.producto = pSobra
        pSobra.save()
        stock.save()
        
        pVenta = Producto()
        pVenta.nombre = "%s %s" % (producto.nombre, fraccion)
        #pVenta.stockTotal = cantiad
        pVenta.descripcion = producto.descripcion
        pVenta.tipoProductoConcreto = producto.tipoProductoConcreto
        pVenta.estrategiaVenta = NoFraccionable()
        pVenta.save()
        return pVenta

# ===================
# = No Fraccionable =
# ===================

class NoFraccionable(Fraccionable):

    class Meta:
        proxy = True

    def instance(self):
        return NoFraccionable.objects.get(pk = ESTRATEGIA_NOFRACCIONABLE)    

    def vender(self, producto, cantidad = None, fraccion = None):
        print "entre a la venta"
        stockLista = producto.stock_set.all()
        for elementoLista in stockLista:
            if elementoLista.disponibles >= cantidad:
                elementoLista.disponibles = elementoLista.disponibles - cantidad
                elementoLista.reservadosNoConfirmados = elementoLista.reservadosNoConfirmados + cantidad
                elementoLista.save()
                break
            else:
                elementoLista.reservadosNoConfirmados = elementoLista.reservadosNoConfirmados + elementoLista.disponibles
                cantidad = cantidad - elementoLista.disponibles                
                elementoLista.disponibles = 0
                elementoLista.save()
                continue
        return producto

    def __unicode__(self):
        return "NoFraccionable"

# =========
# = Stock =
# =========

class Stock(models.Model):
    reservadosComfirmados = models.IntegerField()
    reservadosNoComfirmados = models.IntegerField()
    disponibles = models.IntegerField()
    deposito = models.ForeignKey(Deposito, blank = True)
    producto = models.ForeignKey(Producto)
    
    def crearStock(self, disponibles, deposito, producto):
        """docstring for crearStock"""
        stock =  Stock()
        stock.reservadosComfirmados= 0
        stock.reservadosNoComfirmados= 0
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
    cantidad = models.IntegerField()
    subtotal = models.IntegerField()
    producto = models.ForeignKey(Producto)

# ======================
# = Detalle Nota Venta =
# ======================

class DetalleNotaVenta(Detalle):
    nota = models.ForeignKey('NotaVenta')
    pass
# ===================
# = Detalle Factura =
# ===================

class DetalleFactura(Detalle):
    factura = models.ForeignKey('Factura')
    venta = models.ForeignKey(DetalleNotaVenta)
    pass

# ==============
# = Nota venta =
# ==============

class NotaVenta(models.Model):
    nroNota = models.IntegerField()
    nombre_cliente = models.CharField(max_length = 40)
    apellido_cliente = models.CharField(max_length = 20)
    fecha = models.datetime 
    class Meta:
        permissions = (
            ("venta", "puede vender"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )       

# ===========
# = Factura =
# ===========

class Factura(models.Model):
    nroFactura = models.IntegerField()
    fecha = models.datetime
    formaDePago = models.CharField(max_length = 15)
    precioTotal = models.IntegerField()
    ventaNota = models.ForeignKey(NotaVenta)
    factura = models.ForeignKey('Remito')    

# ==========
# = Remito =
# ==========

class Remito(models.Model):
    nroRemito = models.IntegerField()
    class Meta:
        permissions = (
            ("entregaMateriales", "puede entregar materiales"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )

# ==================
# = Detalle Remito =
# ==================

class DetalleRemito(models.Model):
    cantidad = models.IntegerField()
    entregado = models.BooleanField()
    detalleFactura = models.ForeignKey(DetalleFactura)
    remito = models.ForeignKey(Remito)
    
# =============
# = Descuento =
# =============

class Descuento(models.Model):
    nroDescuento = models.IntegerField()
    fecha = models.datetime
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)

# ============
# = Donacion =
# ============
class Donacion(Descuento):
    beneficiario = models.CharField(max_length = 40)
    
    def __unicode__(self):
        return "%s" % self.beneficiario

# ==========
# = Averia =
# ==========

class Averia(Descuento):
    pass

# ============
# = Extravio =
# ============
class Extravio(Descuento):
    pass

# ========
# = Robo =
# ========

class Robo(Descuento):
    pass