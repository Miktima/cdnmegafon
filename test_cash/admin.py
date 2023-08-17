from django.contrib import admin
from .models import Cash_settings

class Cash_settingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login information', {'fields': ['login', 'password']}),
        ('URLs', {'fields': ['url_auth', 'url_status', 'url_request']}),
    ]

admin.site.register(Cash_settings, Cash_settingsAdmin)

