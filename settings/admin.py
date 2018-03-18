from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'create_timestamp', 'update_timestamp')
    list_display = ('user', 'annual_accrual_days',
                    'remaining_accrual_days')

admin.site.register(Profile, ProfileAdmin)
