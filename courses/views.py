from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Course, Quiz, Choice, Question, Categorie
from assessment.models import Tentative, ReponseUtilisateur
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from gamification.badge_engine import check_and_award
# Create your views here.
_CAT_MODEL = None

def get_cat_model():
    global _CAT_MODEL
    if _CAT_MODEL is None:
        import os
        import joblib
        from django.conf import settings
        model_path = os.path.join(settings.BASE_DIR, 'adaptive_ai', 'cat_model.joblib')
        if os.path.exists(model_path):
            _CAT_MODEL = joblib.load(model_path)
    return _CAT_MODEL

def courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, "courses.html", context)

def coursedetail(request, course_name):
    course = get_object_or_404(Course, name = course_name)
    if request.method == 'POST':
        if not course.students.filter(id = request.user.id).exists():
            course.students.add(request.user)
            return redirect('learn', course_name = course_name)
    context = {
        'course': course
    }
    return render(request, "coursedetail.html", context)

@login_required
def learn(request, course_name):
    course = Course.objects.get(name = course_name)
    context = {
        'course': course
    }
    return render(request, "course.html", context)
@login_required
def quizintro(request, course_name):
    course = Course.objects.get(name=course_name)
    quiz = course.quiz_set.first()
    
    if not quiz:
        quiz, created = Quiz.objects.get_or_create(
            course=course,
            defaults={
                'name': f"Évaluation - {course.name}",
                'time_limit_minutes': 15,
                'max_attempts': 3
            }
        )

    attempts_count = Tentative.objects.filter(user=request.user, quiz=quiz).count()
    max_attempts = quiz.max_attempts
    has_reached_limit = attempts_count >= max_attempts if max_attempts > 0 else False

    context = {
        'course': course,
        'quiz': quiz,
        'attempts_count': attempts_count,
        'max_attempts': max_attempts,
        'has_reached_limit': has_reached_limit,
    }
    return render(request, "quizintro.html", context)

@login_required
def take_quiz(request, course_name):
    course = Course.objects.get(name=course_name)
    quiz = course.quiz_set.first()
    
    if not quiz:
        quiz, created = Quiz.objects.get_or_create(
            course=course,
            defaults={
                'name': f"Évaluation - {course.name}",
                'time_limit_minutes': 15,
                'max_attempts': 3
            }
        )
        
    attempts_count = Tentative.objects.filter(user=request.user, quiz=quiz).count()
    if quiz.max_attempts > 0 and attempts_count >= quiz.max_attempts:
        return redirect('quizintro', course_name=course_name)
        
    attempt = Tentative.objects.create(user=request.user, quiz=quiz, score=0, cheat_alert=False)
        
    from users.models import PlatformSetting
    settings = PlatformSetting.get_settings()

    context = {
        'course': course,
        'quiz': quiz,
        'attempt': attempt,
        'disable_chronometer': settings.disable_chronometer,
    }
    return render(request, "take_quiz.html", context)

@login_required
def api_quiz_action(request, attempt_id):
    attempt = get_object_or_404(Tentative, id=attempt_id, user=request.user)
    quiz = attempt.quiz
    
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        total_questions_in_quiz = quiz.question_set.count()
        if total_questions_in_quiz == 0:
            total_questions_in_quiz = Question.objects.filter(category=quiz.course.categorie).count()
        limit = min(10, total_questions_in_quiz)
        
        if action == 'report_cheat':
            attempt.cheat_alert = True
            attempt.save()
            return JsonResponse({'status': 'success'})
            
        elif action == 'submit_answer':
            question_id = data.get('question_id')
            choice_id = data.get('choice_id')
            time_taken = int(data.get('time_taken', 15))
            
            question = get_object_or_404(Question, id=question_id)
            choice = get_object_or_404(Choice, id=choice_id)
            
            if not ReponseUtilisateur.objects.filter(attempt=attempt, question=question).exists():
                ReponseUtilisateur.objects.create(
                    attempt=attempt,
                    question=question,
                    choice=choice,
                    time_taken=time_taken
                )
                
                from adaptive_ai.models import NiveauCompetence
                from adaptive_ai.elo_engine import update_user_elo
                
                skill_level, created = NiveauCompetence.objects.get_or_create(
                    user=request.user,
                    category=quiz.course.categorie,
                    defaults={'estimated_level': 1200.0}
                )
                
                is_correct = choice.is_correct
                new_elo = update_user_elo(
                    user_rating=skill_level.estimated_level,
                    question_difficulty=question.difficulty_level,
                    is_correct=is_correct
                )
                skill_level.estimated_level = new_elo
                skill_level.save()
            
            total_answered = ReponseUtilisateur.objects.filter(attempt=attempt).count()
            
            if total_answered >= limit:
                correct_count = ReponseUtilisateur.objects.filter(attempt=attempt, choice__is_correct=True).count()
                final_score = int((correct_count / limit) * 100) if limit > 0 else 0
                attempt.score = final_score
                attempt.save()

                request.user.score_global += final_score
                request.user.save()

                new_badges = check_and_award(request.user, attempt)
                request.session['new_badges'] = [b.name for b in new_badges]

                return JsonResponse({
                    'status': 'finished',
                    'redirect': f"/courses/quiz_result/{quiz.course.name}/{attempt.id}",
                })
                
        answered_q_ids = ReponseUtilisateur.objects.filter(attempt=attempt).values_list('question_id', flat=True)
        total_answered = answered_q_ids.count()
        
        if total_answered >= limit:
            correct_count = ReponseUtilisateur.objects.filter(attempt=attempt, choice__is_correct=True).count()
            final_score = int((correct_count / limit) * 100) if limit > 0 else 0
            attempt.score = final_score
            attempt.save()

            request.user.score_global += final_score
            request.user.save()

            new_badges = check_and_award(request.user, attempt)
            request.session['new_badges'] = [b.name for b in new_badges]

            return JsonResponse({
                'status': 'finished',
                'redirect': f"/courses/quiz_result/{quiz.course.name}/{attempt.id}",
            })
            
        from adaptive_ai.models import NiveauCompetence
        skill_level, created = NiveauCompetence.objects.get_or_create(
            user=request.user,
            category=quiz.course.categorie,
            defaults={'estimated_level': 1200.0}
        )
        user_elo = skill_level.estimated_level
        
        quiz_questions = Question.objects.filter(quiz=quiz)
        if quiz_questions.exists():
            available_questions = quiz_questions.exclude(id__in=answered_q_ids)
        else:
            available_questions = Question.objects.filter(category=quiz.course.categorie).exclude(id__in=answered_q_ids)
        
        if total_answered == 0:
            if available_questions.exists():
                next_q = min(available_questions, key=lambda q: abs(q.difficulty_level - user_elo))
            else:
                next_q = None
        else:
            import os
            import joblib
            import pandas as pd
            from django.conf import settings
            
            last_response = ReponseUtilisateur.objects.filter(attempt=attempt).order_by('-id').first()
            last_question_difficulty = last_response.question.difficulty_level if last_response else 1200
            
            correct_count = ReponseUtilisateur.objects.filter(attempt=attempt, choice__is_correct=True).count()
            session_accuracy = (correct_count / total_answered) if total_answered > 0 else 0.0
            
            responses = ReponseUtilisateur.objects.filter(attempt=attempt).order_by('-id')
            streak = 0
            for r in responses:
                if r.choice.is_correct:
                    streak += 1
                else:
                    break
                    
            from django.db.models import Avg
            avg_time_taken = ReponseUtilisateur.objects.filter(attempt=attempt).aggregate(Avg('time_taken'))['time_taken__avg'] or 15
            
            target_difficulty = user_elo
            
            try:
                cat_model = get_cat_model()
                if cat_model is not None:
                    input_data = pd.DataFrame([{
                        'student_base_elo': user_elo,
                        'last_question_difficulty': last_question_difficulty,
                        'session_accuracy': session_accuracy,
                        'current_streak': streak,
                        'avg_time_taken': avg_time_taken
                    }])
                    target_difficulty = cat_model.predict(input_data)[0]
                else:
                    raise Exception("Model not loaded")
            except Exception as e:
                if last_response and last_response.choice.is_correct:
                    target_difficulty = user_elo + 50
                else:
                    target_difficulty = user_elo - 50
            
            if last_response:
                if not last_response.choice.is_correct:
                    max_allowed = min(user_elo, last_question_difficulty)
                    if target_difficulty > max_allowed:
                        target_difficulty = max_allowed - 50
                else:
                    if target_difficulty > user_elo + 150:
                        target_difficulty = user_elo + 50

            if available_questions.exists():
                next_q = min(available_questions, key=lambda q: abs(q.difficulty_level - target_difficulty))
            else:
                next_q = None
        
        if not next_q:
            correct_count = ReponseUtilisateur.objects.filter(attempt=attempt, choice__is_correct=True).count()
            final_score = int((correct_count / total_answered) * 100) if total_answered > 0 else 0
            attempt.score = final_score
            attempt.save()

            request.user.score_global += final_score
            request.user.save()

            new_badges = check_and_award(request.user, attempt)
            request.session['new_badges'] = [b.name for b in new_badges]

            return JsonResponse({'status': 'finished', 'redirect': f"/courses/quiz_result/{quiz.course.name}/{attempt.id}"})
            
        choices = list(next_q.choice_set.values('id', 'text'))
        import random
        random.shuffle(choices)
        
        return JsonResponse({
            'status': 'next_question',
            'question': {
                'id': next_q.id,
                'text': next_q.text,
                'choices': choices,
                'difficulty': next_q.difficulty_level
            },
            'progress': {
                'current': total_answered + 1,
                'total': limit
            }
        })
        
    return JsonResponse({'status': 'error'})

@login_required
def quiz_result(request, course_name, attempt_id):
    attempt = Tentative.objects.get(id=attempt_id, user=request.user)
    course = Course.objects.get(name=course_name)
    
    new_badges = request.session.pop('new_badges', [])
    
    context = {
        'course': course,
        'attempt': attempt,
        'quiz': attempt.quiz,
        'new_badges': new_badges,
    }
    return render(request, "quiz_result.html", context)

@login_required
def create_course(request):
    if request.user.role != 'professeur' and not request.user.is_superuser:
        return redirect('courses')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
        
    context = {
        'form': form
    }
    return render(request, "create_course.html", context)

@login_required
def manage_course(request, course_name):
    course = get_object_or_404(Course, name=course_name, teacher=request.user)
    quiz = course.quiz_set.first()
    context = {
        'course': course,
        'quiz': quiz
    }
    return render(request, "manage_course.html", context)

@login_required
def create_quiz(request, course_name):
    course = get_object_or_404(Course, name=course_name, teacher=request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz = Quiz.objects.create(
                name=data.get('name', f"Quiz - {course.name}"),
                time_limit_minutes=int(data.get('time_limit_minutes', 15)),
                max_attempts=int(data.get('max_attempts', 3)),
                course=course
            )
            
            for q_data in data.get('questions', []):
                question = Question.objects.create(
                    text=q_data.get('text', ''),
                    difficulty_level=int(q_data.get('difficulty', 1200)),
                    quiz=quiz,
                    category=course.categorie
                )
                
                for c_data in q_data.get('choices', []):
                    Choice.objects.create(
                        text=c_data.get('text', ''),
                        is_correct=c_data.get('is_correct', False),
                        question=question
                    )
                    
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return render(request, "create_quiz.html", {'course': course})

@login_required
def edit_quiz(request, course_name):
    course = get_object_or_404(Course, name=course_name, teacher=request.user)
    quiz = get_object_or_404(Quiz, course=course)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz.name = data.get('name', quiz.name)
            quiz.time_limit_minutes = int(data.get('time_limit_minutes', quiz.time_limit_minutes))
            quiz.max_attempts = int(data.get('max_attempts', quiz.max_attempts))
            quiz.save()
            
            quiz.question_set.all().delete()
            
            for q_data in data.get('questions', []):
                question = Question.objects.create(
                    text=q_data.get('text', ''),
                    difficulty_level=int(q_data.get('difficulty', 1200)),
                    quiz=quiz,
                    category=course.categorie
                )
                for c_data in q_data.get('choices', []):
                    Choice.objects.create(
                        text=c_data.get('text', ''),
                        is_correct=c_data.get('is_correct', False),
                        question=question
                    )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    questions_data = []
    for question in quiz.question_set.all():
        choices_data = []
        for choice in question.choice_set.all():
            choices_data.append({
                'text': choice.text,
                'is_correct': choice.is_correct
            })
        questions_data.append({
            'text': question.text,
            'difficulty': question.difficulty_level,
            'choices': choices_data
        })
        
    context = {
        'course': course,
        'quiz': quiz,
        'quiz_data_json': json.dumps({
            'name': quiz.name,
            'time_limit_minutes': quiz.time_limit_minutes,
            'max_attempts': quiz.max_attempts,
            'questions': questions_data
        })
    }
    return render(request, "edit_quiz.html", context)

@login_required
def edit_course(request, course_name):
    course = get_object_or_404(Course, name=course_name, teacher=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            return redirect('manage_course', course_name=course.name)
    else:
        form = CourseForm(instance=course)
        
    context = {
        'course': course,
        'form': form
    }
    return render(request, "edit_course.html", context)


