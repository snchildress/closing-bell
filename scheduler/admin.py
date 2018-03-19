from django.contrib import admin

from .models import Request


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('create_timestamp', 'update_timestamp')
    list_display = ('user', 'number_of_days', 'start_date')

admin.site.register(Request, RequestAdmin)
