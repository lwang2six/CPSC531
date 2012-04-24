from django import forms

from django.forms.widgets import *
from census.models import *
from misc.models import *

class CensusSearchForm(forms.Form):
    age = forms.MultipleChoiceField(label='Age', choices=[('','---Age---')]+[('ANY', 'All age')]+[(v, v) for v in range(1,101)]+[('101', '100+')], widget=SelectMultiple(attrs={}), required=False)
    m_status = forms.MultipleChoiceField(label='Marital Status', choices=[('','---Marital Status---')]+[('ANY', 'All Status')]+[(v.id, v.status) for v in Marital.objects.all()], widget=SelectMultiple(attrs={}),required=False)
    relation = forms.MultipleChoiceField(label='Relationship', choices=[('','---Relationship---')]+[('ANY', 'All relationships')]+[(v.id, v.type) for v in Relationship.objects.all()], widget=SelectMultiple(attrs={}),required=False)
    sex = forms.MultipleChoiceField(label='Sex', choices=[('','---Sex---')]+[('ANY', 'All sex choice')]+[i for i in PERSON_SEXS], widget=SelectMultiple(attrs={}),required=False)
    race = forms.MultipleChoiceField(label='Race', choices=[('','---Race---')]+[('ANY', 'All ethnicity')]+[(v.id, v.ethnicity) for v in Race.objects.all()], widget=SelectMultiple(attrs={}), required=False)
    nc = forms.MultipleChoiceField(label='Native Country', choices=[('','---Native Country---')]+[('ANY', 'All countries')]+[(v.id, v.name) for v in Country.objects.all()], widget=SelectMultiple(attrs={}), required=False)
    
    edu = forms.MultipleChoiceField(label='Education', choices=[('','---Education---')]+[('ANY', 'All education level')]+[(v.id, v.level) for v in Education.objects.all()], widget=SelectMultiple(attrs={}), required=False)

    income = forms.MultipleChoiceField(label='Income', choices=[('', '---Income Level---'), ('ANY', 'All income'), ('>','> 50K'), ('<', '50K >=')], widget=SelectMultiple(attrs={}), required=False)
    occ = forms.MultipleChoiceField(label='Occupation', choices=[('','---Occupation---')]+[('ANY', 'All occupation')]+[(v.id, v.title) for v in Occupation.objects.all()], widget=SelectMultiple(attrs={}),required=False)
    cg = forms.IntegerField(label='Capital Gain', min_value=-1, widget=TextInput(attrs={}), required=False)
    cl = forms.IntegerField(label='Capital Loss', min_value=-1, widget=TextInput(attrs={}), required=False)
    hpw = forms.IntegerField(label='Hours Per Week', min_value=-1, max_value=168, widget=TextInput(attrs={}), required=False)
    wc = forms.MultipleChoiceField(label='Work Class', choices=[('','---Work Class---')]+[('ANY', 'All workclass')]+[(v.id, v.title) for v in WorkClass.objects.all()], widget=SelectMultiple(attrs={}), required=False)

    min_support = forms.IntegerField(label='User Specified Minimum Support', min_value=0, max_value=14, widget=TextInput(attrs={}), required=False)
    
        
