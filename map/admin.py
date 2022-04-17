from django.contrib import admin

# Register your models here.
from map.models import Entry, College

admin.site.register(Entry)
admin.site.register(College)
