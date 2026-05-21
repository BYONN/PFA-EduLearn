from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from users.models import User, PlatformSetting
from courses.models import Course
from courses.forms import CourseForm
from django.contrib.auth.decorators import login_required


def home(request):
    courses = Course.objects.all().order_by('-id')[:2]
    top_students = User.objects.filter(role='etudiant').order_by('-score_global')[:3]
    context = {
        'courses': courses,
        'top_students': top_students,
    }
    return render(request, "home.html", context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Adresse email ou mot de passe incorrect.")
            
    return render(request, "login.html")

def register(request):
    settings = PlatformSetting.get_settings()
    if not settings.allow_registration:
        messages.error(request, "Les inscriptions sont temporairement fermées par l'administrateur.")
        return redirect('login')
        
    contexte = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'errors': {}
    }
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        contexte['username'] = username
        contexte['first_name'] = first_name
        contexte['last_name'] = last_name
        contexte['email'] = email
        errors = {}

        if password and confirm_password and password != confirm_password:
            errors['confirm_password'] = "Les mots de passe ne correspondent pas."
            
        if email and User.objects.filter(email=email).exists():
            errors['email'] = "Un utilisateur avec cet email existe déjà."

        if username and User.objects.filter(username=username).exists():
            errors['username'] = "Un utilisateur avec ce nom d'utilisateur existe déjà."
            
        if not errors:
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role='etudiant'
            )
            user.set_password(password)
            user.save()
            
            messages.success(request, "Compte créé avec succès ! Veuillez vous connecter.")
            return redirect('login')
            
        contexte['errors'] = errors

    return render(request, "register.html", contexte)

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import user_passes_test
from users.models import User, PlatformSetting

@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_settings':
            settings = PlatformSetting.get_settings()
            settings.allow_registration = request.POST.get('allow_registration') == 'on'
            settings.display_leaderboard = request.POST.get('display_leaderboard') == 'on'
            settings.disable_chronometer = request.POST.get('disable_chronometer') == 'on'
            settings.maintenance_mode = request.POST.get('maintenance_mode') == 'on'
            settings.max_quiz_attempts = request.POST.get('max_quiz_attempts', 3)
            settings.save()
            messages.success(request, "Paramètres sauvegardés avec succès.")
            return redirect('admin_panel')
            
        elif action == 'change_role':
            user_id = request.POST.get('user_id')
            new_role = request.POST.get('role')
            target_user = get_object_or_404(User, id=user_id)
            if target_user == request.user:
                messages.error(request, "Vous ne pouvez pas modifier votre propre rôle.")
            else:
                target_user.role = new_role
                target_user.save()
                messages.success(request, f"Rôle de {target_user.username} mis à jour avec succès ({new_role}).")
            return redirect('admin_panel')
            
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            target_user = get_object_or_404(User, id=user_id)
            if target_user == request.user:
                messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            else:
                username = target_user.username
                target_user.delete()
                messages.success(request, f"Utilisateur {username} supprimé avec succès.")
            return redirect('admin_panel')
            
        elif action == 'reset_cheat_alert':
            attempt_id = request.POST.get('attempt_id')
            attempt = get_object_or_404(Tentative, id=attempt_id)
            attempt.cheat_alert = False
            attempt.save()
            messages.success(request, f"Alerte de triche réinitialisée pour {attempt.user.username}.")
            return redirect('admin_panel')

    users = User.objects.all()
    
    students_count = sum(1 for u in users if u.role == 'etudiant' or 'etudiant' in u.role or u.role == '{}' or u.role == '')
    professors_count = sum(1 for u in users if u.role == 'professeur' or 'professeur' in u.role)
    course_count = Course.objects.count()
    settings = PlatformSetting.get_settings()
    
    # Load cheating attempts for Security tab
    cheat_attempts = Tentative.objects.filter(cheat_alert=True).select_related('user', 'quiz__course')

    context = {
        'users': users,
        'total_users': users.count(),
        'students_count': students_count,
        'professors_count': professors_count,
        'course_count': course_count,
        'settings': settings,
        'cheat_attempts': cheat_attempts,
    }
    return render(request, "admin_panel.html", context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'professeur' and not request.user.is_superuser:
        return redirect('courses')
        
    courses = Course.objects.filter(teacher=request.user)
    context = {
        'courses': courses
    }
    return render(request, "teacher_dashboard.html", context)

from assessment.models import Tentative

def leaderboard(request):
    """Top students ranked by global score."""
    settings = PlatformSetting.get_settings()
    if not settings.display_leaderboard:
        return render(request, 'leaderboard.html', {'disabled': True})
        
    top_users = User.objects.filter(role='etudiant').order_by('-score_global')[:20]
    context = {
        'top_users': top_users,
    }
    return render(request, 'leaderboard.html', context)

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    attempts = (
        Tentative.objects.filter(user=user)
        .select_related('quiz__course')
        .order_by('-started_at')
    )

    passed = attempts.filter(score__gte=50).count()
    failed = attempts.filter(score__lt=50).count()
    total  = attempts.count()
    avg_score = (
        int(sum(a.score for a in attempts) / total) if total > 0 else 0
    )

    user_badges = user.userbadge_set.select_related('badge').order_by('-unlocked_at')

    from adaptive_ai.models import NiveauCompetence
    competences = NiveauCompetence.objects.filter(user=user).select_related('category')

    context = {
        'profile_user': user,
        'attempts': attempts[:10],   
        'passed': passed,
        'failed': failed,
        'total': total,
        'avg_score': avg_score,
        'user_badges': user_badges,
        'competences': competences,
    }
    return render(request, 'profile.html', context)
