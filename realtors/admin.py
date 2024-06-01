from django.contrib import admin
from .models import Realtor

class RealtorAdmin (admin.ModelAdmin):
    list_display = ('id' ,'sname', 'email', 'hire_date')
    list_display_links = ('id', 'sname')
    search_fields = ('sname',)
    list_per_page = 25

admin.site.register(Realtor, RealtorAdmin)