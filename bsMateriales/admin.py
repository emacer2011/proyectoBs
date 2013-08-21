from django.contrib import admin
from bsMateriales.models import NotaVenta, DetalleNotaVenta, Producto, Rubro, Stock, TipoProducto, Deposito, Fraccionable, Remito, Factura, DetalleFactura, DetalleRemito, EstrategiaVenta, NoFraccionable

admin.site.register(TipoProducto)
admin.site.register(Rubro)
admin.site.register(Deposito)
admin.site.register(Fraccionable)
admin.site.register(Stock)
admin.site.register(Remito)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(DetalleRemito)
admin.site.register(NoFraccionable)
admin.site.register(EstrategiaVenta)
class StockInline(admin.TabularInline):
    model = Stock

class StockAdmin(admin.ModelAdmin):
    inlines = [StockInline]


class DetalleNotaVentaInline(admin.TabularInline):
    model = DetalleNotaVenta
     
class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleNotaVentaInline]

admin.site.register(NotaVenta, VentaAdmin)
admin.site.register(Producto, StockAdmin)