import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduLearn.settings")
django.setup()

from courses.models import Course, Categorie, Quiz, Question, Choice

def seed_python1_quiz():
    # 1. Fetch Course "Python 1"
    try:
        course = Course.objects.get(name="Python 1")
    except Course.DoesNotExist:
        try:
            course = Course.objects.get(id=1)
        except Course.DoesNotExist:
            print("Error: Could not find Python 1 course.")
            return

    category = course.categorie
    print(f"Targeting Course: '{course.name}' | Category: '{category.name}'")

    # 2. Get or Create the Quiz for this Course
    quiz, created = Quiz.objects.get_or_create(
        course=course,
        defaults={
            'name': f"Quiz d'évaluation - {course.name}",
            'time_limit_minutes': 15,
            'max_attempts': 3
        }
    )
    if created:
        print(f"Created new Quiz: {quiz.name}")
    else:
        print(f"Using existing Quiz: {quiz.name}")

    # 3. Clean up existing questions on this quiz to avoid duplicate seeds
    deleted_quiz_count, _ = Question.objects.filter(quiz=quiz).delete()
    print(f"Cleaned up {deleted_quiz_count} existing quiz questions.")

    # 4. Define the 5 realistic introductory questions covering variables, basic types, inputs/outputs, and logical conditions.
    questions_data = [
        {
            "text": "<p>Comment Python exécute-t-il généralement son code source ?</p>",
            "difficulty": 400,
            "choices": [
                {"text": "Il est interprété ligne par ligne au moment de l'exécution.", "is_correct": True},
                {"text": "Il est entièrement compilé en code machine binaire avant l'exécution.", "is_correct": False},
                {"text": "Il nécessite obligatoirement d'être exécuté dans un navigateur web.", "is_correct": False},
                {"text": "Il ne s'exécute que sur des bases de données SQL.", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le type de la variable <code>x</code> après l'instruction <code>x = \"3.14\"</code> ?</p>",
            "difficulty": 500,
            "choices": [
                {"text": "str (chaîne de caractères)", "is_correct": True},
                {"text": "float (nombre à virgule flottante)", "is_correct": False},
                {"text": "int (nombre entier)", "is_correct": False},
                {"text": "bool (booléen)", "is_correct": False}
            ]
        },
        {
            "text": "<p>Par défaut, quel est le type de données renvoyé par la fonction intégrée <code>input()</code> en Python ?</p>",
            "difficulty": 600,
            "choices": [
                {"text": "Toujours une chaîne de caractères (str)", "is_correct": True},
                {"text": "Un nombre entier (int) ou flottant (float) selon la saisie", "is_correct": False},
                {"text": "Un booléen (bool)", "is_correct": False},
                {"text": "Une liste d'éléments", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'évaluation et de l'affichage du code suivant ?</p><pre><code class=\"language-python\">x = 10\nprint(x > 5 and x < 10)</code></pre>",
            "difficulty": 700,
            "choices": [
                {"text": "False (car x n'est pas strictement inférieur à 10)", "is_correct": True},
                {"text": "True", "is_correct": False},
                {"text": "None", "is_correct": False},
                {"text": "Une erreur de syntaxe", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle est la syntaxe correcte pour tester si une variable <code>age</code> est supérieure ou égale à 18 en Python ?</p>",
            "difficulty": 800,
            "choices": [
                {"text": "if age >= 18:", "is_correct": True},
                {"text": "if (age >= 18) {", "is_correct": False},
                {"text": "if age >= 18 then", "is_correct": False},
                {"text": "if age => 18:", "is_correct": False}
            ]
        }
    ]

    # 5. Insert questions
    for idx, q_item in enumerate(questions_data, 1):
        question = Question.objects.create(
            text=q_item["text"],
            difficulty_level=q_item["difficulty"],
            quiz=quiz,
            category=category
        )
        print(f"[{idx}/5] Created Question (ELO {q_item['difficulty']})")
        
        for c_item in q_item["choices"]:
            Choice.objects.create(
                text=c_item["text"],
                is_correct=c_item["is_correct"],
                question=question
            )

    print("\nSuccessfully populated 5 introductory Python questions for the 'Python 1' quiz!")

if __name__ == "__main__":
    seed_python1_quiz()
