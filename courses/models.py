from django.db import models
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    color = ColorField(default='#000000')
    def __str__(self):
        return self.name
        
class Course(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField(max_length = 500)
    content = RichTextUploadingField()
    teacher = models.ForeignKey('users.User', related_name='taught_courses', on_delete=models.CASCADE)
    students = models.ManyToManyField('users.User', related_name='enrolled_courses', blank=True)
    cover_image = models.ImageField(upload_to='course_covers/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Quiz(models.Model):
    name = models.CharField(max_length = 100)
    time_limit_minutes = models.IntegerField()
    max_attempts = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Question(models.Model):
    text = RichTextUploadingField()
    difficulty_level = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)
class Choice(models.Model):
    text = models.CharField(max_length = 100)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)