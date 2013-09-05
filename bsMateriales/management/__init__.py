from django.db.models.signals import post_syncdb
import bsMateriales.models
from bsMateriales.models import NoFraccionable, ESTRATEGIA_NOFRACCIONABLE, Rubro, TipoProducto, Producto
from django.contrib.auth.models import Group, User, Permission

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

    
    #GRUPOS POR DEFECTO
    #################################################
    grupo, created = Group.objects.get_or_create(name='CAJERO')
    if created:
        print 'grupo CAJERO creado '
    
    permiso = Permission.objects.get(name='puede cobrar')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    grupo.save()
    #################################################
    grupo, created = Group.objects.get_or_create(name='VENDEDORES')
    if created:
        print 'grupo VENDEDORES creado '
    
    permiso = Permission.objects.get(name='puede vender')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    grupo.save()
    #################################################
    grupo, created = Group.objects.get_or_create(name='ADMINISTRATIVO')
    if created:
        print 'grupo ADMINISTRATIVO creado'
    
    permiso = Permission.objects.get(name='puede manejar abm Deposito')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    grupo.save()

    #################################################
    grupo, created = Group.objects.get_or_create(name='ENCARGADO-DEPOSITO')
    if created:
        print 'grupo ENCARGADO-DEPOSITO creado'
    permiso = Permission.objects.get(name='puede cargar/eliminar stock')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    permiso = Permission.objects.get(name='puede entregar materiales')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    permiso = Permission.objects.get(name='puede manejar abm Producto')#agregamos el permiso
    grupo.permissions.add(permiso) #agregamos el permiso
    grupo.save()


post_syncdb.connect(crearSingleton, sender=bsMateriales.models)
        