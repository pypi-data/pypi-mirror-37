from django.contrib import admin
from .models import Configuration

# Register your models here.
class PaasAdmin(admin.ModelAdmin):
    list_display = ('end_point', 'trigger', 'default')
    list_editable = ['default']

admin.site.register(Configuration)