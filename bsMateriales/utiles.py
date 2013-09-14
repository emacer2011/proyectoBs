
from bsMateriales.models import Factura, DetalleFactura

class AdaptadorFactura():
    """"""
    pk = None
    nombreCliente = None
    apellidoCliente = None
    ventaNota = None
    detalles = None
    fecha = None
    total = None

    def inicializar(self, notaVenta):
    	self.factura = Factura.objects.get(ventaNota = notaVenta)
    	self.pk = self.factura.pk
    	self.fecha = self.factura.fecha
    	self.total = self.factura.precioTotal
    	self.ventaNota = self.factura.ventaNota
    	self.apellidoCliente = self.factura.ventaNota.apellidoCliente
    	self.nombreCliente = self.factura.ventaNota.nombreCliente
    	self.detalles = DetalleFactura.objects.filter(factura = self.factura)

    

        