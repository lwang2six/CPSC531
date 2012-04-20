from django.conf.urls.defaults import *
from django.utils.importlib import import_module
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
    (r'^', include('census.urls')),
    (r'^', include('record.urls')),

)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^%s(?P<path>.*)$' % settings.STATIC_PREFIX, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^media/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT + '/css/'}, name='css-root'),
    ) + urlpatterns
