from django.db.models.query import QuerySet
from systemtest.people.models import *
from django.contrib.auth import get_user_model
from django.utils.timezone import now


def get_users_leads():
    return get_user_model().objects.filter(groups__name="LEAD")


def get_users_department(department__name: str, order_by: str = "") -> QuerySet:
    users = get_user_model().objects.filter(
        department__name=department__name
    )
    if order_by:
        return users.order_by(order_by)
    return users


def get_user_as_choice():
    choices = []
    for user in get_users_department("PRUEBAS", "last_name"):
        choices.append(
            (user, f"{user.last_name} {user.first_name} [ {user.username} ]"))
    return choices


def get_user_requirements_summary(user) -> dict[str, str]:
    requirements = PeopleRequirement.objects.filter(
        for_user=user, start__year=now().year
    )

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

    for key, value in summary_dict.items():
        summary_dict[key] = str(summary_dict[key]) if summary_dict[key] else ""

    return summary_dict


def get_requirements_summary():
    summary = {}
    for user in get_users_department("PRUEBAS"):
        summary[user] = get_user_requirements_summary(user)

    return summary
