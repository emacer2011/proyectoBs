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
    url(r'^venta/$', 'bsMateriales.views.venta'),
    url(r'^login/$', 'bsMateriales.views.login_user'),
    url(r'^deslogear/$', 'bsMateriales.views.deslogear'),
    url(r'^listarDeposito/$', 'bsMateriales.views.listarDeposito'),
    url(r'^cargarStock/$', 'bsMateriales.views.cargarStock'),
    url(r'^altaProducto/$', 'bsMateriales.views.altaProducto'),
    url(r'^entregaMateriales/$', 'bsMateriales.views.entregaMateriales'),
    url(r'^cobro/$', 'bsMateriales.views.cobro'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )