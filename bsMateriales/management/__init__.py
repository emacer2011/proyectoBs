from django.db.models.signals import post_syncdb
import bsMateriales.models
from bsMateriales.models import NoFraccionable, ESTRATEGIA_NOFRACCIONABLE, Rubro, TipoProducto, Producto

print("ENTRO PARA ACA")
def crearSingleton(sender, **kwargs):

    #estrategia, created = NoFraccionable.objects.get_or_create(pk = ESTRATEGIA_NOFRACCIONABLE, 
    #defaults = {"medida":0, "minimo":0})

    estrategia = NoFraccionable()
    estrategia.pk = ESTRATEGIA_NOFRACCIONABLE
    estrategia.save()
    print estrategia, ","


    
    #RUBRO POR DEFECTO
    rubro = Rubro()
    rubro.inicializar("Construccion","Construccion",1)
    rubro.save()
    print rubro, ","

    #TIPO DE PRODUCTO CREADO POR DEFECTO
    tipoProducto = TipoProducto()
    tipoProducto.inicializar("Material de Construccion","Materiales",1,"Metros", 1)
    tipoProducto.save()
    #tipo, created = TipoProducto.objects.get_or_create(pk = 1, defaults = {"nombre":"Material de construccion", 
    #                "unidadMedida": 1, "rubro": rubro})
    print tipoProducto, ","



post_syncdb.connect(crearSingleton, sender=bsMateriales.models)
        