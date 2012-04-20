from django.contrib import admin

from misc.models import *

class RaceAdmin(admin.ModelAdmin):
    list_display = ('ethnicity',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class OccupationAdmin(admin.ModelAdmin):
    list_display = ('title',)

class EducationAdmin(admin.ModelAdmin):
    list_display = ('level',)

class MaritalAdmin(admin.ModelAdmin):
    list_display = ('status',)

class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('type',)

class WorkClassAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Race, RaceAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Marital, MaritalAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(WorkClass, WorkClassAdmin)
