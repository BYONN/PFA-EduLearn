from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PlatformSetting

class CustomUserAdmin(UserAdmin):
    # This adds your custom fields to the beautiful default Django User Admin page
    list_display = UserAdmin.list_display + ('role', 'score_global')
    fieldsets = UserAdmin.fieldsets + (
        ('Gamification & Roles', {'fields': ('role', 'score_global')}),
    )

class PlatformSettingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allow_registration', 'display_leaderboard', 'disable_chronometer', 'maintenance_mode')
    list_editable = ('allow_registration', 'display_leaderboard', 'disable_chronometer', 'maintenance_mode')

admin.site.register(PlatformSetting, PlatformSettingAdmin)
admin.site.register(User, CustomUserAdmin)