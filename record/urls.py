from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^records/(?P<rid>\d+)/$', 'record.views.record_run_detail'),
    (r'^records/$', 'record.views.record_run_list'),
)
