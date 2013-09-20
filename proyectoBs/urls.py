from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyectoBs.views.home', name='home'),
    # url(r'^proyectoBs/', include('proyectoBs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'bsMateriales.views.index'),
    url(r'^altaDeposito/$', 'bsMateriales.views.altaDeposito'),
    url(r'^bajaDeposito/$', 'bsMateriales.views.bajaDeposito'),
    url(r'^modificarDeposito/$', 'bsMateriales.views.modificarDeposito'),
    url(r'^altaProducto/$', 'bsMateriales.views.altaProducto'),   
    url(r'^bajaProducto/$', 'bsMateriales.views.bajaProducto'),
    url(r'^modificarProducto/$', 'bsMateriales.views.modificarProducto'),
    url(r'^venta/$', 'bsMateriales.views.venta'),
    url(r'^login/$', 'bsMateriales.views.login_user'),
    url(r'^deslogear/$', 'bsMateriales.views.deslogear'),
    url(r'^listarDeposito/$', 'bsMateriales.views.listarDeposito'),
    url(r'^listarDepositoPDF/$', 'bsMateriales.views.listarDepositoPDF'),        
    url(r'^listarProducto/$', 'bsMateriales.views.listarProducto'),
    url(r'^listarProductoPDF/$', 'bsMateriales.views.listarProductoPDF'),        
    url(r'^cargarStock/$', 'bsMateriales.views.cargarStock'),    
    url(r'^entregaMateriales/$', 'bsMateriales.views.entregaMateriales'),
    url(r'^cobro/$', 'bsMateriales.views.cobro'),
    url(r'^actualizarEntregados/$', 'bsMateriales.views.actualizarEntregados'),
    url(r'^cargarDetalles/$', 'bsMateriales.views.cargarDetalles'),
    url(r'^cargarEntregados/$', 'bsMateriales.views.cargarEntregados'),
    url(r'^cargarDepositos/$', 'bsMateriales.views.cargarDepositos'),
    url(r'^actualizarStocks/$', 'bsMateriales.views.actualizarStocks'),
    url(r'^generarFactura/$', 'bsMateriales.views.generarFactura'),
    url(r'^ayudaVenta/$', 'bsMateriales.views.ayudaVenta'),
    url(r'^ayudaAltaProducto/$', 'bsMateriales.views.ayudaAltaProducto'),
    url(r'^ayudaBajaProducto/$', 'bsMateriales.views.ayudaBajaProducto'),
    url(r'^ayudaModificarProducto/$', 'bsMateriales.views.ayudaModificarProducto'),
    url(r'^ayudaListarProducto/$', 'bsMateriales.views.ayudaListarProductos'),
    url(r'^ayudaAltaDeposito/$', 'bsMateriales.views.ayudaAltaDeposito'),
    url(r'^ayudaBajaDeposito/$', 'bsMateriales.views.ayudaBajaDeposito'),
    url(r'^ayudaModificarDeposito/$', 'bsMateriales.views.ayudaModificarDeposito'),
    url(r'^ayudaListarDepositos/$', 'bsMateriales.views.ayudaListarDepositos'),
    url(r'^ayudaEntregaMateriales/$', 'bsMateriales.views.ayudaEntregaMateriales'),
    url(r'^ayudaManejoStock/$', 'bsMateriales.views.ayudaManejoStock'),
    url(r'^ayudaCobro/$', 'bsMateriales.views.ayudaCobro'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )