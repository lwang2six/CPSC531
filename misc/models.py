from django.db import models

#add primary keys for all tables.
class Race(models.Model):
    ethnicity = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ethnicity

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Occupation(models.Model):
    title = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Education(models.Model):
    level = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.level

class Marital(models.Model):
    status = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.status

class Relationship(models.Model):
    type = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.type

class WorkClass(models.Model):
    title = models.CharField(max_length=255, unique=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
