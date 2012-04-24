# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

from django.contrib import messages

from apriori.utils import *
from census.models import *
from census.forms import *

def flatpage(request, p_name=None):
    template = 'index.html'
    if p_name:
        if p_name == 'about':
            template = '%s.html' % p_name
        else:
            raise Http404

    return direct_to_template(request, template, {})

#need to change to GET...THOUGHTS?
def census_data(request, p_name=''):
    form = CensusSearchForm()
    template = 'census_list.html'
    if p_name:
        if p_name not in ['person', 'workclass', 'education']:
            messages.info(request, 'No such page')
            return HttpResponseRedirect('/census/')
        template = '%s.html' % p_name

    census_list = Person.objects.all()
    paginator = Paginator(census_list, 200)

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    
    try:
        census = paginator.page(page)
    except EmptyPage:
        census = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        min_support = ''
        form = CensusSearchForm(data=request.POST)
        if form.is_valid():
            q = ()
            s = ''
            f  = []
    
            if request.POST.get('age'):
                if request.POST.get('age') != 'ANY':
                    q += (Q(age=request.POST.get('age')),)
                s += '%s:%s,' % ('age', request.POST.get('age'))
                f.append('%s:%s,' % ('age', request.POST.get('age')))

            if request.POST.get('m_status'):
                try:
                    if request.POST.get('m_status') != 'ANY':
                        m = Martial.objects.get(id=request.POST.get('m_status'))
                        q += (Q(martial_status__id=m.id),)
                    else:
                        m = None
                    s += '%s:%s,' % ('marital_status', m.status if m else 'ANY')
                    f.append('%s:%s,' % ('marital_status', m.id if m else 'ANY'))
                except:
                    pass
    
            if request.POST.get('relation'):
                try:
                    if request.POST.get('relation') != 'ANY':
                        x = Relationship.objects.get(id=request.POST.get('relation'))
                        q += (Q(relationship__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('relationship', x.type if x else 'ANY')
                    f.append('%s:%s,' % ('relationship', x.id if x else 'ANY'))
                except:
                    pass
    
            if request.POST.get('sex'):
                sex = x = request.POST.get('sex')
                if sex != 'ANY':
                    if sex == 'm':
                        x = 'Male'
                    else:
                        x = 'Female' if sex == 'F' else 'Other'
                    q += (Q(sex=request.POST.get('sex')),)
                s += '%s:%s,' % ('sex', x)
                f.append('%s:%s,' % ('sex', x[0]))

            if request.POST.get('race'):
                try:
                    if request.POST.get('race') != 'ANY':
                        x = Race.objects.get(id=request.POST.get('race'))
                        q += (Q(race__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('race', x.ethnicity if x else 'ANY')
                    f.append('%s:%s,' % ('race', x.id if x else 'ANY'))
                except:
                    pass
    
            if request.POST.get('nc'):
                try:
                    if request.POST.get('nc') != 'ANY':
                        x = Country.objects.get(id=request.POST.get('nc'))
                        q += (Q(native_country__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('native_country', x.name if x else 'ANY')
                    f.append('%s:%s,' % ('native_country', x.id if x else 'ANY'))
                except:
                    pass
    
            if request.POST.get('edu'):
                try:
                    if request.POST.get('age') != 'ANY':
                        x = Education.objects.get(id=request.POST.get('edu'))
                        q += (Q(education__education__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('education', x.level if x else 'ANY')
                    f.append('%s:%s,' % ('education', x.id if x else 'ANY'))
                except: 
                    pass

            if request.POST.get('income'):
                try:
                    if request.POST.get('income') == '-1':
                        s += 'income:ANY,'
                        f.append('income:ANY,')
                    else:
                        q += (Q(work__income=request.POST.get('income')),)
                        s += '%s:%s,' % ('income', 'True' if request.POST.get('income') else 'False')
                        f.append('%s:%s,' % ('income', 'True' if request.POST.get('income') else 'False'))
                except:
                    pass

            if request.POST.get('occ'):
                try:
                    if request.POST.get('occ') != 'ANY':
                        x = Occupation.objects.get(id=request.POST.get('occ'))
                        q += (Q(work__occupation__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('occupation', x.title if x else 'ANY')
                    f.append('%s:%s,' % ('occupation', x.id if x else 'ANY'))
                except:
                    pass
    
            if request.POST.get('cg') != '':
                print request.POST.get('cg')
                print dir(request.POST.get('cg'))
                try:
                    if request.POST.get('cg') == '-1':
                        s += 'capital_gain:ANY,'
                        f.append('capital_gain:ANY,')
                    else:
                        q += (Q(work__capital_gain=request.POST.get('cg')),)
                        s += '%s:%s,' % ('capital_gain', request.POST.get('cg'))
                        f.append('%s:%s,' % ('capital_gain', request.POST.get('cg')))
                except:
                    pass
    
            if request.POST.get('cl') != '':
                try:
                    if request.POST.get('cl') == '-1':
                        s += 'capital_loss:ANY,'
                        f.append('capital_loss:ANY,')
                    else:
                        q += (Q(work__capital_loss=request.POST.get('cl')),)
                        s += '%s:%s,' % ('capital_loss', request.POST.get('cl'))
                        f.append('%s:%s,' % ('capital_loss', request.POST.get('cl')))
                except:
                    pass
            if request.POST.get('hpw') !=  '':
                try:
                    if request.POST.get('hpw') == '-1':
                        s += 'hours_per_week:ANY,'
                        f.append('hours_per_week:ANY,')
                    else:
                        q += (Q(work__hours_per_week=request.POST.get('hpw')),)
                        s += '%s:%s,' % ('hours_per_week', request.POST.get('hpw'))
                        f.append('%s:%s,' % ('hours_per_week', request.POST.get('hpw')))
                except:
                    pass

            if request.POST.get('wc'):
                try:
                    if request.POST.get('age') != 'ANY':
                        x = Workclass.objects.get(id=request.POST.get('wc'))
                        q += (Q(work__workclass__id=x.id),)
                    else:
                        x = None
                    s += '%s:%s,' % ('workclass', x.title if x else 'ANY')  
                    f.append('%s:%s,' % ('workclass', x.id if x else 'ANY'))
                except:
                    pass

            if request.POST.get('min_support'):
                min_support = '?min_support='
    
                if len(f) < request.POST.get('min_support'):
                    min_support += str(len(f))
                    messages.info(request, 'Error with "User Minimum Support Value" - Support value cannot be greater then the amount of fields selected, it has been defaulted to the amount of fields selected.')
                else:
                    min_support += str(request.POST.get('min_support'))

            return HttpResponseRedirect('%s%s' % (apriori(q, s, f), min_support))

    return direct_to_template(request, template, {
                                       'census':census,
                                       'form':form,
                                      })
