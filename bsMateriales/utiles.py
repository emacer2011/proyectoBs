
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

    def setDetalles(self, detalles):
        diccionario = {}
        for detalle in detalles:
            if diccionario.has_key(detalle.producto):
                    d = diccionario.get(detalle.producto)
                    d.cantidad = d.cantidad + detalle.cantidad
                    d.subtotal=  d.subtotal+ detalle.subtotal
                    del diccionario[detalle.producto]
                    diccionario[detalle.producto]= d
            else:
                diccionario[detalle.producto] = detalle 

        self.detalles = diccionario.values()


    def inicializar(self, notaVenta):
    	self.factura = Factura.objects.get(ventaNota = notaVenta)
    	self.pk = self.factura.pk
    	self.fecha = self.factura.fecha
    	self.total = self.factura.precioTotal
    	self.ventaNota = self.factura.ventaNota
    	self.apellidoCliente = self.factura.ventaNota.apellidoCliente
    	self.nombreCliente = self.factura.ventaNota.nombreCliente
    	self.setDetalles( DetalleFactura.objects.filter(factura = self.factura))

    

        