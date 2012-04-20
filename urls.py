from django.conf.urls.defaults import *
from django.utils.importlib import import_module

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
    (r'^', include('census.urls')),
    (r'^', include('record.urls')),

)
