from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    role=models.CharField(max_length=50,default='etudiant')
    score_global=models.IntegerField(default=0)

class PlatformSetting(models.Model):
    allow_registration = models.BooleanField(default=True)
    display_leaderboard = models.BooleanField(default=True)
    disable_chronometer = models.BooleanField(default=False)
    maintenance_mode = models.BooleanField(default=False)
    max_quiz_attempts = models.IntegerField(default=3)

    def __str__(self):
        return "Paramètres de la plateforme"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj