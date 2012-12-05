from django.db.models.signals import post_syncdb
import bsMateriales.models
from bsMateriales.models import NoFraccionable, ESTRATEGIA_NOFRACCIONABLE, Rubro, TipoProducto, Producto

print("ENTRO PARA ACA")
def crearSingleton(sender, **kwargs):

    estrategia, created = NoFraccionable.objects.get_or_create(pk = ESTRATEGIA_NOFRACCIONABLE, 
        defaults = {"medida":0, "minimo":0})
    print estrategia, ",", created
    
    rubro, created = Rubro.objects.get_or_create(pk = 1, defaults = {"nombre":"Construccion"})
    print rubro, ",", created

    tipo, created = TipoProducto.objects.get_or_create(pk = 1, defaults = {"nombre":"Material de construccion", 
                    "unidadMedida": 1, "rubro": rubro})
    print tipo, ",", created
post_syncdb.connect(crearSingleton, sender=bsMateriales.models)
        