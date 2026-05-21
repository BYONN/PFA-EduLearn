from django.contrib import admin
from .models import Course, Quiz, Question, Choice, Categorie

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'time_limit_minutes', 'max_attempts')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'difficulty_level')
    list_filter = ('quiz', 'difficulty_level')

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Categorie, CategorieAdmin)
