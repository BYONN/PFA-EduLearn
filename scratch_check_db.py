import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduLearn.settings")
django.setup()

from courses.models import Course, Quiz, Question, Categorie

print("--- Quizzes and Questions ---")
for course in Course.objects.all():
    print(f"Course: {course.name} (ID: {course.id})")
    quizzes = course.quiz_set.all()
    print(f"  Quizzes count: {quizzes.count()}")
    for quiz in quizzes:
        q_count = quiz.question_set.count()
        print(f"    Quiz: {quiz.name} (ID: {quiz.id}) | Direct Questions Count: {q_count}")
        for question in quiz.question_set.all():
            print(f"      - Question ID: {question.id} | Elo: {question.difficulty_level} | Text: {question.text[:60]}")
    
    # Also show questions associated with the category
    cat = course.categorie
    if cat:
        cat_q_count = Question.objects.filter(category=cat, quiz=None).count()
        print(f"    Category: {cat.name} | Shared Questions (quiz=None) Count: {cat_q_count}")
        for question in Question.objects.filter(category=cat, quiz=None):
            print(f"      - Shared Question ID: {question.id} | Elo: {question.difficulty_level} | Text: {question.text[:60]}")
    print()
