import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduLearn.settings")
django.setup()

from courses.models import Course, Categorie, Quiz, Question, Choice

def seed_questions():
    # 1. Fetch Course and Category
    try:
        course = Course.objects.get(name="Exam Python")
    except Course.DoesNotExist:
        course = Course.objects.get(id=4)
        
    category = course.categorie
    print(f"Targeting Course: '{course.name}' | Category: '{category.name}'")

    # 2. Get or Create the Quiz for this Course
    quiz, created = Quiz.objects.get_or_create(
        course=course,
        defaults={
            'name': f"Quiz Général - {course.name}",
            'time_limit_minutes': 15,
            'max_attempts': 3
        }
    )
    if created:
        print(f"Created new Quiz: {quiz.name}")
    else:
        print(f"Using existing Quiz: {quiz.name}")

    # 3. Clean up existing questions on this quiz and the Python category to avoid duplicates
    deleted_quiz_count, _ = Question.objects.filter(quiz=quiz).delete()
    deleted_cat_count, _ = Question.objects.filter(category=category).delete()
    print(f"Cleaned up {deleted_quiz_count} quiz questions and {deleted_cat_count} category questions.")

    # 4. Define the 30 dynamic ELO questions
    questions_data = [
        # --- EASY (ELO 800 - 1000) ---
        {
            "text": "<p>Quel est le résultat de la fonction <code>type([])</code> en Python ?</p>",
            "difficulty": 850,
            "choices": [
                {"text": "<class 'list'>", "is_correct": True},
                {"text": "<class 'dict'>", "is_correct": False},
                {"text": "<class 'tuple'>", "is_correct": False},
                {"text": "<class 'array'>", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle fonction intégrée permet d'obtenir la longueur d'une liste ou d'une chaîne de caractères ?</p>",
            "difficulty": 900,
            "choices": [
                {"text": "len()", "is_correct": True},
                {"text": "length()", "is_correct": False},
                {"text": "size()", "is_correct": False},
                {"text": "count()", "is_correct": False}
            ]
        },
        {
            "text": "<p>Comment débute un commentaire sur une seule ligne en Python ?</p>",
            "difficulty": 800,
            "choices": [
                {"text": "Le caractère #", "is_correct": True},
                {"text": "Le symbole //", "is_correct": False},
                {"text": "Le symbole /*", "is_correct": False},
                {"text": "Le tag <!--", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'expression suivante en console Python ?</p><pre><code class=\"language-python\">3 * 'A'</code></pre>",
            "difficulty": 950,
            "choices": [
                {"text": "'AAA'", "is_correct": True},
                {"text": "3", "is_correct": False},
                {"text": "'A3'", "is_correct": False},
                {"text": "Une erreur de type TypeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle est la différence fondamentale entre une liste (<code>list</code>) et un tuple (<code>tuple</code>) en Python ?</p>",
            "difficulty": 880,
            "choices": [
                {"text": "La liste est mutable (modifiable), alors que le tuple est immuable", "is_correct": True},
                {"text": "Le tuple est mutable, alors que la liste est immuable", "is_correct": False},
                {"text": "Le tuple peut contenir différents types d'éléments, la liste non", "is_correct": False},
                {"text": "La liste s'écrit avec des parenthèses, le tuple avec des crochets", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'instruction <code>list(range(3))</code> en Python ?</p>",
            "difficulty": 920,
            "choices": [
                {"text": "[0, 1, 2]", "is_correct": True},
                {"text": "[1, 2, 3]", "is_correct": False},
                {"text": "[0, 1, 2, 3]", "is_correct": False},
                {"text": "Une erreur de type TypeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Lequel de ces noms de variables est <strong>invalide</strong> en Python ?</p>",
            "difficulty": 820,
            "choices": [
                {"text": "2_variables", "is_correct": True},
                {"text": "_variable2", "is_correct": False},
                {"text": "variable_deux", "is_correct": False},
                {"text": "VARIABLE", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'opération modulo <code>7 % 3</code> en Python ?</p>",
            "difficulty": 860,
            "choices": [
                {"text": "1 (car 7 divisé par 3 fait 2, avec un reste de 1)", "is_correct": True},
                {"text": "2", "is_correct": False},
                {"text": "2.33", "is_correct": False},
                {"text": "0", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'instruction <code>\"python\".capitalize()</code> ?</p>",
            "difficulty": 910,
            "choices": [
                {"text": "'Python'", "is_correct": True},
                {"text": "'PYTHON'", "is_correct": False},
                {"text": "'python'", "is_correct": False},
                {"text": "Une erreur de type AttributeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'opération suivante en console Python ?</p><pre><code class=\"language-python\">[1, 2] * 2</code></pre>",
            "difficulty": 940,
            "choices": [
                {"text": "[1, 2, 1, 2]", "is_correct": True},
                {"text": "[2, 4]", "is_correct": False},
                {"text": "[[1, 2], [1, 2]]", "is_correct": False},
                {"text": "Une erreur de type TypeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Si une fonction ne contient aucune instruction <code>return</code> explicite, que retourne-t-elle par défaut en Python ?</p>",
            "difficulty": 980,
            "choices": [
                {"text": "None", "is_correct": True},
                {"text": "0", "is_correct": False},
                {"text": "False", "is_correct": False},
                {"text": "Une erreur de type AttributeError", "is_correct": False}
            ]
        },
        
        # --- MEDIUM (ELO 1100 - 1400) ---
        {
            "text": "<p>Quel est le résultat du code suivant ?</p><pre><code class=\"language-python\">x = [1, 2, 3]\ny = x\ny.append(4)\nprint(len(x))</code></pre>",
            "difficulty": 1200,
            "choices": [
                {"text": "4", "is_correct": True},
                {"text": "3", "is_correct": False},
                {"text": "5", "is_correct": False},
                {"text": "Une erreur de type AttributeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle méthode permet d'ajouter un élément à la fin d'une liste existante ?</p>",
            "difficulty": 1100,
            "choices": [
                {"text": "append()", "is_correct": True},
                {"text": "add()", "is_correct": False},
                {"text": "insert()", "is_correct": False},
                {"text": "extend()", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'opérateur division entière (<code>5 // 2</code>) en Python ?</p>",
            "difficulty": 1150,
            "choices": [
                {"text": "2", "is_correct": True},
                {"text": "2.5", "is_correct": False},
                {"text": "2.0", "is_correct": False},
                {"text": "1", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'expression booléenne suivante ?</p><pre><code class=\"language-python\">bool(\"False\")</code></pre>",
            "difficulty": 1300,
            "choices": [
                {"text": "True", "is_correct": True},
                {"text": "False", "is_correct": False},
                {"text": "None", "is_correct": False},
                {"text": "Une erreur de syntaxe", "is_correct": False}
            ]
        },
        {
            "text": "<p>Dans le dictionnaire suivant, quel est le résultat de l'instruction <code>d.get(\"age\", 25)</code> ?</p><pre><code class=\"language-python\">d = {\"nom\": \"Alice\", \"ville\": \"Paris\"}</code></pre>",
            "difficulty": 1250,
            "choices": [
                {"text": "25 (car la clé 'age' n'existe pas, la valeur par défaut est renvoyée)", "is_correct": True},
                {"text": "None", "is_correct": False},
                {"text": "Une erreur de type KeyError", "is_correct": False},
                {"text": "25, et la clé 'age' est insérée dans d", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'exécution de ce script ?</p><pre><code class=\"language-python\">x = 10\ndef modifier():\n    global x\n    x = 20\nmodifier()\nprint(x)</code></pre>",
            "difficulty": 1350,
            "choices": [
                {"text": "20", "is_correct": True},
                {"text": "10", "is_correct": False},
                {"text": "Une erreur de type NameError", "is_correct": False},
                {"text": "None", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de cette compréhension de liste ?</p><pre><code class=\"language-python\">[x**2 for x in range(5) if x % 2 == 0]</code></pre>",
            "difficulty": 1400,
            "choices": [
                {"text": "[0, 4, 16]", "is_correct": True},
                {"text": "[1, 9]", "is_correct": False},
                {"text": "[0, 1, 4, 9, 16]", "is_correct": False},
                {"text": "[4, 16]", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'instruction de découpage (slicing) suivante ?</p><pre><code class=\"language-python\">\"hello\"[::-1]</code></pre>",
            "difficulty": 1120,
            "choices": [
                {"text": "'olleh'", "is_correct": True},
                {"text": "'hello'", "is_correct": False},
                {"text": "'o'", "is_correct": False},
                {"text": "Une erreur de type IndexError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'intersection de ces deux ensembles en Python ?</p><pre><code class=\"language-python\">a = {1, 2, 3}\nb = {2, 3, 4}\nprint(a & b)</code></pre>",
            "difficulty": 1180,
            "choices": [
                {"text": "{2, 3}", "is_correct": True},
                {"text": "{1, 2, 3, 4}", "is_correct": False},
                {"text": "{1, 4}", "is_correct": False},
                {"text": "None", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'affichage de ce dictionnaire contenant des doublons de clés ?</p><pre><code class=\"language-python\">d = {\"a\": 1, \"b\": 2, \"a\": 3}\nprint(d[\"a\"])</code></pre>",
            "difficulty": 1220,
            "choices": [
                {"text": "3 (la dernière clé 'a' écrase la valeur précédente)", "is_correct": True},
                {"text": "1", "is_correct": False},
                {"text": "[1, 3]", "is_correct": False},
                {"text": "Une erreur de type KeyError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'exécution de ce script de copie de liste ?</p><pre><code class=\"language-python\">a = [1, 2, 3]\nb = a[:]\nb.append(4)\nprint(len(a))</code></pre>",
            "difficulty": 1280,
            "choices": [
                {"text": "3 (car le slicing [:] crée une copie superficielle de la liste)", "is_correct": True},
                {"text": "4", "is_correct": False},
                {"text": "5", "is_correct": False},
                {"text": "Une erreur de type AttributeError", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'évaluation de cette expression booléenne combinant and et or ?</p><pre><code class=\"language-python\">True or False and False</code></pre>",
            "difficulty": 1380,
            "choices": [
                {"text": "True (car l'opérateur 'and' a une priorité plus élevée que 'or')", "is_correct": True},
                {"text": "False", "is_correct": False},
                {"text": "None", "is_correct": False},
                {"text": "Une erreur de type TypeError", "is_correct": False}
            ]
        },
        
        # --- HARD (ELO 1500 - 1800) ---
        {
            "text": "<p>Quel est le résultat de l'exécution de ce code ?</p><pre><code class=\"language-python\">def func(a, b=[]):\n    b.append(a)\n    return b\n\nprint(func(1))\nprint(func(2))</code></pre>",
            "difficulty": 1550,
            "choices": [
                {"text": "[1, 2] (la liste par défaut est partagée)", "is_correct": True},
                {"text": "[2] uniquement", "is_correct": False},
                {"text": "[1] puis [2] séparément", "is_correct": False},
                {"text": "Une erreur de compilation", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle est la complexité temporelle moyenne pour vérifier la présence d'une clé dans un dictionnaire Python (<code>key in dict</code>) ?</p>",
            "difficulty": 1600,
            "choices": [
                {"text": "O(1)", "is_correct": True},
                {"text": "O(log n)", "is_correct": False},
                {"text": "O(n)", "is_correct": False},
                {"text": "O(n log n)", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel décorateur est utilisé pour déclarer une méthode qui reçoit la classe parente (cls) en premier argument plutôt que l'instance ?</p>",
            "difficulty": 1500,
            "choices": [
                {"text": "@classmethod", "is_correct": True},
                {"text": "@staticmethod", "is_correct": False},
                {"text": "@property", "is_correct": False},
                {"text": "@classmethodself", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'exécution de ce bloc d'instructions ?</p><pre><code class=\"language-python\">a = (1, 2, [3, 4])\ntry:\n    a[2].append(5)\n    print(\"Success\")\nexcept TypeError:\n    print(\"Error\")</code></pre>",
            "difficulty": 1700,
            "choices": [
                {"text": "Success (les listes à l'intérieur d'un tuple restent mutables)", "is_correct": True},
                {"text": "Error (le tuple est immuable)", "is_correct": False},
                {"text": "Le programme crashe sans rien afficher", "is_correct": False},
                {"text": "SyntaxError à la ligne 1", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel dictionnaire est généré par cette expression en Python ?</p><pre><code class=\"language-python\">{x: x * 2 for x in range(3)}</code></pre>",
            "difficulty": 1520,
            "choices": [
                {"text": "{0: 0, 1: 2, 2: 4}", "is_correct": True},
                {"text": "{1: 2, 2: 4, 3: 6}", "is_correct": False},
                {"text": "[0, 2, 4]", "is_correct": False},
                {"text": "{0: 0, 1: 1, 2: 2}", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quelle est la principale différence entre l'expression <code>[x for x in range(1000)]</code> et <code>(x for x in range(1000))</code> ?</p>",
            "difficulty": 1650,
            "choices": [
                {"text": "Le premier génère une liste complète en mémoire, le second est un générateur qui évalue les éléments à la demande", "is_correct": True},
                {"text": "Le premier est plus rapide mais consomme plus, le second est immuable", "is_correct": False},
                {"text": "Le second est une erreur de syntaxe en Python", "is_correct": False},
                {"text": "Le premier retourne une liste, le second retourne un tuple complet", "is_correct": False}
            ]
        },
        {
            "text": "<p>Quel est le résultat de l'exécution de ce code ?</p><pre><code class=\"language-python\">a = 256\nb = 256\nc = 300\nd = 300\nprint(a is b, c is d)</code></pre>",
            "difficulty": 1750,
            "choices": [
                {"text": "True False (car Python met en cache les petits entiers de -5 à 256)", "is_correct": True},
                {"text": "True True", "is_correct": False},
                {"text": "False False", "is_correct": False},
                {"text": "Une erreur de syntaxe", "is_correct": False}
            ]
        }
    ]

    # 5. Insert them into the global category pool (quiz=None)
    total_q = len(questions_data)
    for q_idx, q_item in enumerate(questions_data, 1):
        question = Question.objects.create(
            text=q_item["text"],
            difficulty_level=q_item["difficulty"],
            quiz=None,
            category=category
        )
        print(f"[{q_idx}/{total_q}] Created Global Question (ELO {q_item['difficulty']})")
        
        for c_item in q_item["choices"]:
            Choice.objects.create(
                text=c_item["text"],
                is_correct=c_item["is_correct"],
                question=question
            )

    print(f"\nAll {total_q} high-quality Python questions successfully populated!")

if __name__ == "__main__":
    seed_questions()
