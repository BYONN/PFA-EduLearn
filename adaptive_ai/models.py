from django.db import models
from users.models import User
from courses.models import Categorie
# Create your models here.
class NiveauCompetence(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    estimated_level = models.FloatField(default = 1200.0)

