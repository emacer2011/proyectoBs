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
    url(r'^venta/$', 'bsMateriales.views.venta'),
    url(r'^login/$', 'bsMateriales.views.login_user'),
    url(r'^deslogear/$', 'bsMateriales.views.deslogear'),
    url(r'^listarDeposito/$', 'bsMateriales.views.listarDeposito'),
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG and settings.STATIC_ROOT:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), 
            'django.views.static.serve',
            {'document_root' : settings.STATIC_ROOT }),)
