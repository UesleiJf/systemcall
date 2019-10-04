from django.contrib import admin
from .models import RegisterCall


class RegisterCallAdmin(admin.ModelAdmin):
    list_display = ['type_call', 'timestamp_call', 'id_call', 'source_call', 'destination_call']


admin.site.register(RegisterCall, RegisterCallAdmin)
