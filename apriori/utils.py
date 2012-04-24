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



def create_subset2(person, record, search_fields, fields):
    temp = set()
    subset = set()
    f_subset = set()

    for i in fields:
        field = i.split(':')[0]
        s = f = ''
        if field == 'age':
            s = 'p.age=%s' % person.age
            f = 'age:%s' % person.age
        elif field == 'marital_status':
            s = 'p.marital_status_id=%s' % person.marital_status.id
            f = 'marital_status:%s' % person.marital_status.status
        elif field == 'relationship':
            s = 'p.relationship_id=%s' % person.relationship.id
            f = 'relationship:%s' % person.relationship.type
        elif field == 'sex':
            s = 'p.sex="%s"' % person.sex
            f = 'sex:%s' % person.get_sex_display()
        elif field == 'race':
            s = 'p.race_id=%s' % person.race.id
            f = 'race:%s' % person.race.ethnicity
        elif field == 'native_country':
            s = 'p.native_country_id=%s' % person.native_country.id
            f = 'native_country:%s' % person.native_country.name
        elif field == 'education':
            s = 'e.education_id=%s' % person.education.education.id
            f = 'education:%s' % person.education.education.level
        elif field == 'income':
            s = 'w.income=%s' % int(person.work.income)
            f = 'income:%s' % int(person.work.income)
        elif field == 'occupation':
            s = 'w.occupation_id=%s' % person.work.occupation.id
            f = 'occupation:%s' % person.work.occupation.title
        elif field == 'capital_gain':
            s = 'w.capital_gain=%s' % person.work.capital_gain
            f = 'capital_gain:%s' % person.work.capital_gain
        elif field == 'capital_loss':
            s = 'w.capital_loss=%s' % person.work.capital_loss
            f = 'capital_loss:%s' % person.work.capital_loss
        elif field == 'hours_per_week':
            s = 'w.hours_per_week=%s' % person.work.hours_per_week
            f = 'hours_per_week:%s' % person.work.hours_per_week
        else: #'workclass':
            s = 'w.workclass_id=%s' % person.work.workclass.id
            f = 'workclass:%s' % person.work.workclass.title
        
        temp = set()
        for k in f_subset:
            temp.add('%s,%s' % (k, f))

        f_subset.add('%s' % f)
        f_subset = f_subset.union(temp)

        temp = set()

        for j in subset:
            temp.add('%s and %s' % (j, s))
        
        subset.add('%s' % s)
        subset = subset.union(temp)

    count = 0
    f_subset = list(f_subset)
    for i in subset:
        try:
            sub = Subset.objects.get(record=record, fields=f_subset[count])
        except:
            raw_s = 'SELECT p.*, count(distinct p.census_person_id) AS total FROM census_person p, census_education e, census_work w where p.census_person_id=e.person_id and p.census_person_id=w.person_id and %s;' % i
            p = Person.objects.raw(raw_s)
            sub = Subset.objects.create(record=record, fields=f_subset[count], first_user=person, occurance=p[0].total, weight=len(f_subset[count].split(',')))

            if sub.weight > record.weight:
                sub.record.weight = sub.weight
                sub.record.save()
        count = count + 1


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
            create_subset2(person, record, search_fields, fields_set)
            #c = c + 1
            #for i in range(c, len(census)):
            #    create_subset(person, record, get_fields(person, census[i], fields_set))
                
        end = datetime.datetime.now()
        record.run_time = (end-start).total_seconds()
        record.save()

        
    return record.get_absolute_url()


