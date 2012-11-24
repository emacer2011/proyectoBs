from django.contrib import admin
from bsMateriales.models import NotaVenta, DetalleNotaVenta, Producto, Rubro, Stock, TipoProducto, Deposito, Fraccionable

admin.site.register(TipoProducto)
admin.site.register(Rubro)
admin.site.register(Deposito)
admin.site.register(Fraccionable)

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