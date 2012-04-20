from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from django.contrib import messages

from record.models import *

def record_run_list(request):
    records = Record.objects.all()
    return direct_to_template(request, 'run_list.html', {'records':records})


def record_run_detail(request, rid):
    record = get_object_or_404(Record,pk=rid)
    result = record.get_subsets().order_by('-weight')

    if request.GET.get('min_support'):
        try: 
            min_support = int(request.GET.get('min_support'))
            result = result.filter(weight__lte=min_support)
        except:
            messages.info(request, 'Error with "User Minimum Support Value"')
            return HttpResponseRedirect(record.get_absolute_url())

    return direct_to_template(request, 'run_detail.html', {'record':record, 'result':result, })
    
