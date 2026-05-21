from django.contrib import admin
from .models import Tentative, ReponseUtilisateur

class TentativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'started_at', 'cheat_alert')
    list_filter = ('cheat_alert', 'quiz')

class ReponseUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'choice', 'time_taken')

admin.site.register(Tentative, TentativeAdmin)
admin.site.register(ReponseUtilisateur, ReponseUtilisateurAdmin)
