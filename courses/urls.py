from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name = 'courses'),
    path('create/', views.create_course, name='create_course'),
    path('learn/<str:course_name>', views.learn, name='learn'),
    path('quizintro/<str:course_name>', views.quizintro, name = 'quizintro'),
    path('take_quiz/<str:course_name>', views.take_quiz, name='take_quiz'),
    path('quiz_result/<str:course_name>/<int:attempt_id>', views.quiz_result, name='quiz_result'),
    path('<str:course_name>/manage/', views.manage_course, name='manage_course'),
    path('<str:course_name>/edit/', views.edit_course, name='edit_course'),
    path('<str:course_name>/quiz/create/', views.create_quiz, name='create_quiz'),
    path('<str:course_name>/quiz/edit/', views.edit_quiz, name='edit_quiz'),
    path('<str:course_name>', views.coursedetail, name='coursedetail'),
    path('api/quiz/action/<int:attempt_id>', views.api_quiz_action, name='api_quiz_action'),
]