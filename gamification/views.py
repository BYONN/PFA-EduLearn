from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from assessment.models import Tentative

User = get_user_model()


def leaderboard(request):
    """Top students ranked by global score."""
    top_users = User.objects.filter(role='etudiant').order_by('-score_global')[:20]
    context = {
        'top_users': top_users,
    }
    return render(request, 'gamification/leaderboard.html', context)


@login_required
def profile(request):
    """Student personal stats — quiz history, badges, score."""
    user = request.user

    attempts = (
        Tentative.objects.filter(user=user, cheat_alert=False)
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

    context = {
        'attempts': attempts[:10],   # show last 10
        'passed': passed,
        'failed': failed,
        'total': total,
        'avg_score': avg_score,
        'user_badges': user_badges,
    }
    return render(request, 'gamification/profile.html', context)
