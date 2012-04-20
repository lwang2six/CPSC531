from django.contrib import admin

from record.models import *

class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'selected_fields', 'weight', 'run_time')

class SubsetAdmin(admin.ModelAdmin):
    list_display = ('id', 'record', 'fields', 'occurance')


admin.site.register(Record, RecordAdmin)
admin.site.register(Subset, SubsetAdmin)

