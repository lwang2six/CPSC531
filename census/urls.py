from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'census.views.index'),
    (r'^census/$', 'census.views.census_data'),
)
