from django.db import models
from courses.models import Choice, Question, Quiz
from users.models import User
# Create your models here.
class Tentative(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    cheat_alert = models.BooleanField(default = False)

class ReponseUtilisateur(models.Model):
    attempt = models.ForeignKey(Tentative, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    time_taken = models.IntegerField(default = 0)