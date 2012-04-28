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
        if p_name == 'about' or p_name == 'sitemap':
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
    
            if request.POST.getlist('age'):
                if 'ANY' not in request.POST.getlist('age'):
                    q += (Q(age__in=request.POST.getlist('age')),)
                for i in request.POST.getlist('age'):
                    s += '%s:%s,' % ('age', i)
                f.append('%s:%s,' % ('age', 'selected' if 'ANY' not in request.POST.getlist('age') else 'ANY' ))
            if request.POST.get('m_status'):
                try:
                    if 'ANY' not in request.POST.getlist('m_status'):
                        m = Marital.objects.filter(id__in=request.POST.getlist('m_status'))
                        q += (Q(martial_status__id__in=m.values('id')),)
                        for i in m:
                            s += '%s:%s,' % ('marital_status', i.status )
                        f.append('%s:%s,' % ('marital_status', 'selected'))
                    else:
                        s += 'marital_status:ANY,'
                        f.append('marital_status:ANY,')
                except:
                    pass
    
            if request.POST.get('relation'):
                try:
                    if 'ANY' not in request.POST.getlist('relation'):
                        x = Relationship.objects.filter(id__in=request.POST.getlist('relation'))
                        q += (Q(relationship__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('relationship', x.type )
                        f.append('%s:%s,' % ('relationship', 'selected'))
                    else:
                        x = None
                        s += 'relationship:ANY,'
                        f.append('relationship:ANY,')
                except:
                    pass

            if request.POST.get('sex'):
                sex = x = request.POST.getlist('sex')
                if 'ANY' not in sex:
                    q += (Q(sex__in=sex),)
                    for i in sex:
                        if sex == 'm':
                            x = 'Male'
                        else:
                            x = 'Female' if sex == 'F' else 'Other'
                        s += '%s:%s,' % ('sex', x)
                    f.append('%s:%s,' % ('sex', 'selected'))
                else:
                    s += 'sex:ANY,'
                    f.append('sex:ANY,')

            if request.POST.get('race'):
                try:
                    if 'ANY' not in request.POST.getlist('race'):
                        x = Race.objects.get(id__in=request.POST.getlist('race'))
                        q += (Q(race__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('race', i.ethnicity)
                        f.append('%s:%s,' % ('race', 'selected'))
                    else:
                        s += 'race:ANY,'
                        f.append('race:ANY,')
                except:
                    pass
    
            if request.POST.get('nc'):
                try:
                    if 'ANY' not in request.POST.getlist('nc'):
                        x = Country.objects.filter(id__in=request.POST.getlist('nc'))
                        q += (Q(native_country__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('native_country', i.name)
                        f.append('%s:%s,' % ('native_country', 'selected'))
                    else:
                        s += '%s:%s,' % ('native_country', 'ANY')
                        f.append('%s:%s,' % ('native_country', 'ANY'))
                except:
                    pass
    
            if request.POST.get('edu'):
                try:
                    if 'ANY' not in request.POST.getlist('edu'):
                        x = Education.objects.filter(id__in=request.POST.getlist('edu'))
                        q += (Q(education__education__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('education', i.level)
                        f.append('%s:%s,' % ('education', 'selected'))
                    else:
                        s += '%s:%s,' % ('education', 'ANY')
                        f.append('%s:%s,' % ('education','ANY'))
                except: 
                    pass

            if request.POST.get('income'):
                try:
                    if '-1' in request.POST.getlist('income'):
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
                    if 'ANY' not in  request.POST.get('occ'):
                        x = Occupation.objects.get(id__in=request.POST.getlist('occ'))
                        q += (Q(work__occupation__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('occupation', i.title)
                        f.append('%s:%s,' % ('occupation', 'selected'))
                    else:
                        s += '%s:%s,' % ('occupation', 'ANY')
                        f.append('%s:%s,' % ('occupation', 'ANY'))
                except:
                    pass
    
            if request.POST.get('cg') != '':
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
                    if 'ANY' not in  request.POST.get('wc'):
                        x = Workclass.objects.getlist(id__in=request.POST.getlist('wc'))
                        q += (Q(work__workclass__id__in=x.values('id')),)
                        for i in x:
                            s += '%s:%s,' % ('workclass', i.title )  
                        f.append('%s:%s,' % ('workclass', 'selected'))
                    else:
                        s += '%s:%s,' % ('workclass', 'ANY')  
                        f.append('%s:%s,' % ('workclass', 'ANY'))
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
                                       'c_page':page,
                                      })
