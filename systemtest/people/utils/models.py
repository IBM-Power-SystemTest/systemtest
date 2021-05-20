from systemtest.people.models import *
from django.contrib.auth import get_user_model
from django.utils.timezone import now


def get_users_leads():
    return get_user_model().objects.filter(groups__name="LEAD")


def get_user_requirements_summary(user) -> dict[str, int]:
    requirements = PeopleRequirement.objects.filter(
        for_user=user, start__year=now().year)

    dict_keys = [
        "VACACIONES",
        "FALTA",
        "FALTA_INJUSTIFICADA",
        "SUSPENSION",
        "RETARDO",
        "OTRO",
    ]
    summary_dict = {key: 0 for key in dict_keys}

    for requirement in requirements:
        r_type = requirement.type.name
        r_days = requirement.days

        try:
            summary_dict[r_type] += r_days
        except KeyError:
            summary_dict["OTRO"] += r_days

    return summary_dict


def get_requirements_summary():
    summary = []
    for user in get_users_leads():
        summary.append({
            "user": user,
            "requirements": get_user_requirements_summary(user)}
        )

    return summary
