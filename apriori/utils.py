import datetime
from django.db.models import Q
from census.models import *
from record.models import *

def get_fields(person1, person2, fields):
    s = []
    first_attribute = None
    for field in fields:
        attribute  = field.split(':')
        if attribute[0] in ('education', 'education_num'):
            first_attribute = 'education'
        elif attribute[0] in ('income', 'occupation', 'capital_gain', 'captial_loss', 'hours_per_week', 'workclass'):
            first_attribute = 'work'

        if first_attribute:
            p1 = person1.get_attribute(first_attribute)
            p2 = person2.get_attribute(first_attribute)
        else:
            p1 = person1
            p2 = person2

        if p1.get_attribute(attribute[0]) == p2.get_attribute(attribute[0]):
                s.append('%s:%s' % (attribute[0], p1.get_attribute(attribute[0])))
    return s

def create_subset(person, record, fields):
    temp = set()
    subset = set()
    for i in fields:
        for j in subset:
            temp.add('%s,%s' % (j, i))

        subset.add('%s' % i)
        subset = subset.union(temp)

    for i in subset:
        try:
            s = Subset.objects.get(record=record, fields=i)
            if s.first_user == person:
                s.occurance = s.occurance + 1
                s.save()
        except:
            s = Subset.objects.create(record=record, fields=i, first_user=person,occurance=2, weight=len(i.split(',')))
            if s.weight > record.weight:
                s.record.weight = s.weight
                s.record.save()

    return True

def apriori(query_list, search_fields, fields_set):

    try:
        record = Record.objects.get(selected_fields=search_fields)
    except:
        record = None

    if record == None:
        record = Record(selected_fields=search_fields)
        record.save()
        q = None

        if len(query_list) == len(fields_set):
            for i in query_list:
                q = q | i if q else i

        census = Person.objects.filter(q) if q else Person.objects.all()

        c = 0
        start = datetime.datetime.now()
        for person in census:
            c = c + 1
            for i in range(c, len(census)):
                create_subset(person, record, get_fields(person, census[i], fields_set))
                
        end = datetime.datetime.now()
        record.run_time = (end-start).total_seconds()
        record.save()

        
    return record.get_absolute_url()


