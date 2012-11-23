from django.contrib import admin
from bsMateriales.models import Rubro, Deposito, Producto, TipoProducto


admin.site.register(Rubro)
admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(Deposito)