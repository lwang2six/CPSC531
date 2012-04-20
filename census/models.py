from django.db import models

from misc.models import *

PERSON_SEX_MALE = 'M'
PERSON_SEX_FEMALE = 'F'
PERSON_SEX_OTHER = 'O'

PERSON_SEXS = (
    (PERSON_SEX_MALE, 'Male'),
    (PERSON_SEX_FEMALE, 'Female'),
    (PERSON_SEX_OTHER, 'Other'),
)

#add census person as primary key
class Person(models.Model):
    census_person_id = models.IntegerField(primary_key=True, unique=True)
    age = models.PositiveIntegerField()
    marital_status = models.ForeignKey(Marital)
    relationship = models.ForeignKey(Relationship)
    sex = models.CharField(max_length=1, choices=PERSON_SEXS)
    race = models.ForeignKey(Race)
    native_country = models.ForeignKey(Country)

    def __unicode__(self):
        return '%s: %s, %s' % (self.census_person_id, self.age, self.sex)

    def get_attribute(self, attrib):
        try:
            return self.__getattribute__(attrib)
        except:
            return None

#remove education_num duplicate 
class Education(models.Model):
    person = models.OneToOneField(Person)
    education = models.ForeignKey(Education) #change to level

    def get_attribute(self, attrib):
        try:
            return self.__getattribute__(attrib)
        except:
            return None

class Work(models.Model):
    person = models.OneToOneField(Person)
    income = models.BooleanField(verbose_name='> 50K', default=False)
    occupation = models.ForeignKey(Occupation)
    capital_gain = models.IntegerField()
    capital_loss = models.IntegerField()
    hours_per_week = models.PositiveIntegerField()
    workclass = models.ForeignKey(WorkClass)

    def get_attribute(self, attrib):
        try:
            return self.__getattribute__(attrib)
        except:
            return None
