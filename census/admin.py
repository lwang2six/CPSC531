from django.contrib import admin

from census.models import *

class PersonAdmin(admin.ModelAdmin):
    list_display = ('census_person_id', 'age', 'marital_status', 'relationship', 'sex', 'native_country')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('person', 'education')

class WorkAdmin(admin.ModelAdmin):
    list_display = ('person', 'income', 'occupation', 'workclass')


admin.site.register(Person, PersonAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Work, WorkAdmin)

