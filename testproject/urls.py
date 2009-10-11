from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^', include('pypi_vanity.urls')),
    ('^$', 'django.views.generic.simple.redirect_to', {'url': '/packages'}),
    (r'^admin/(.*)', admin.site.root)
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
