from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    (r'^$', 'census.views.flatpage'),
    (r'^census/(?P<p_name>\w+)/$', 'census.views.census_data'),
    (r'^census/$', 'census.views.census_data'),
    (r'^(?P<p_name>\w+)/$', 'census.views.flatpage'),
)
