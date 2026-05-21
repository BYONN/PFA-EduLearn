"""
Badge Engine — automatically checks and awards badges to a user
after a quiz attempt is completed.
"""
from .models import Badge, UserBadge
from assessment.models import Tentative


BADGE_DEFINITIONS = {
    "premiere_victoire": {
        "name": "Premiére Victoire",
        "description": "Réussir un quiz pour la premiére fois.",
        "image": "badges/firstquiz.png",
    },
    "parfait": {
        "name": "Parfait",
        "description": "Obtenir 100% à un quiz.",
        "image": "badges/perfect.png",
    },
}


def _get_or_create_badge(slug):
    defn = BADGE_DEFINITIONS[slug]
    badge, _ = Badge.objects.get_or_create(
        name=defn["name"],
        defaults={
            "description": defn["description"],
            "image": defn["image"],
        },
    )
    return badge


def _award(user, slug):
    badge = _get_or_create_badge(slug)
    _, created = UserBadge.objects.get_or_create(user=user, badge=badge)
    return created


def check_and_award(user, attempt):

    newly_awarded = []

    if attempt.cheat_alert:
        return newly_awarded

    score = attempt.score

    if score >= 50:
        passed_count = Tentative.objects.filter(
            user=user, score__gte=50, cheat_alert=False
        ).count()
        if passed_count >= 1:
            if _award(user, "premiere_victoire"):
                newly_awarded.append(_get_or_create_badge("premiere_victoire"))

    if score == 100:
        if _award(user, "parfait"):
            newly_awarded.append(_get_or_create_badge("parfait"))


   
    return newly_awarded
