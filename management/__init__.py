from django.db.models.signals import post_syncdb
import bsMateriales.models
from bsMateriales.models import NoFraccionable, ESTRATEGIA_NOFRACCIONABLE

print("ENTRO PARA ACA")
def crearSingleton(sender, **kwargs):
    print NoFraccionable.objects.get_or_create(pk = ESTRATEGIA_NOFRACCIONABLE, 
        defaults = {"medida":0, "minimo":0})
    print NoFraccionable, sender, kwargs

post_syncdb.connect(crearSingleton, sender=bsMateriales.models)
        