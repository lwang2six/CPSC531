from django.db import models

from census.models import Person

class Record(models.Model):
    selected_fields = models.TextField()
    weight = models.PositiveIntegerField(default=0)
    
    run_time = models.DecimalField(max_digits=65, decimal_places=15, default=0)

    def __unicode__(self):
        return '%s' % self.id

    def get_absolute_url(self):
        return '/records/%s/' % self.id

    def get_weighted_total(self):
        return Subset.objects.filter(record__id=self.id, count=self.weight).aggregate(models.Sum('occurance'))

    def get_subsets(self):
        return Subset.objects.filter(record__id=self.id).order_by('occurance')

class Subset(models.Model):
    record = models.ForeignKey(Record)
    fields = models.CharField(max_length=512)
    occurance = models.IntegerField(default=0)
    first_user = models.ForeignKey(Person)
    weight = models.IntegerField(default=0)

    class Meta:
        unique_together = (('record', 'fields'),)

    def __unicode__(self):
        return '%s: [%s] - %s' % (self.record, self.fields, self.occurance)


