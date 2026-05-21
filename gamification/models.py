from django.db import models
from users.models import User
# Create your models here.

class Badge(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    image = models.ImageField(upload_to = 'badges')

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

