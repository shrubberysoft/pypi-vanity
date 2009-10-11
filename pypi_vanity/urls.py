from django.conf.urls.defaults import patterns

urlpatterns = patterns('pypi_vanity.views',
    ('^packages$', 'package_index')
)
