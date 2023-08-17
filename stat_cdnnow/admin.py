from django.contrib import admin
from .models import Portals_stat, Stat_settings

class Stat_settingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login information', {'fields': ['login', 'password']}),
        ('Client', {'fields': ['client_id']}),
        ('URLs', {'fields': ['url_stat', 'url_auth']}),
    ]

admin.site.register(Portals_stat)
admin.site.register(Stat_settings, Stat_settingsAdmin)
