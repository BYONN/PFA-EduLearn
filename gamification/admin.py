from django.contrib import admin
from .models import Badge, UserBadge

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')

class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'unlocked_at')
# Register your models here.
admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
