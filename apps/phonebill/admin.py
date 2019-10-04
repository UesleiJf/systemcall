from django.contrib import admin
from .models import Registers


class RegisterAdmin(admin.ModelAdmin):
    list_display = ['phone_origin', 'period_call', 'destination_call', 'duration_call',
                    'price_call', 'start_date_call', 'start_time_call']


admin.site.register(Registers, RegisterAdmin)
