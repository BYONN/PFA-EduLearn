from django.contrib import admin
from .models import NiveauCompetence

class NiveauCompetenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'estimated_level')
    list_filter = ('category',)

admin.site.register(NiveauCompetence, NiveauCompetenceAdmin)
