from typing import Any, Type
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction, IntegrityError
from django.db.models import Model


from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from systemtest.users.models import Job, Department
from systemtest.pts.models import RequestGroupWorkspace, RequestStatus

User = get_user_model()


options = {
    RequestGroupWorkspace: (
        {"name": "P/I SERIES"},
        {"name": "EARLY BUILD"},
        {"name": "CSC"},
    ),

    RequestStatus: (
        {"name": "OPEN"},
        {"name": "CANCEL"},
        {"name": "TRANSIT"},
        {"name": "PENDING"},
        {"name": "RETURN"},
        {"name": "GOOD"},
        {"name": "BAD"},
        {"name": "INSTALADO EN OTRA WU"},
        {"name": "REVISION CON EL ME"},
        {"name": "CLOSE GOOD"},
        {"name": "CLOSE BAD"},
        {"name": "VALIDANDO INVENTARIO"},
        {"name": "SOLICITADO A OTRA AREA"},
        {"name": "CORTO REAL"},
        {"name": "SOLICITADO A DE GEODIS"},
        {"name": "NUMERO DE PARTE NO EXISTE"},
        {"name": "VPD BURN"},
        {"name": "NUMERO DE PARTE NO VALIDO"},
    ),

    Department: (
        {"name": "PRUEBAS"},
        {"name": "CONTROL DE MATERIALES"},
        {"name": "EARLY BUILD"},
        {"name": "MES"},
        {"name": "CSC"},
    ),

    Job: (
        {"name": "TA"},
        {"name": "TA TRAINER"},
        {"name": "TA IBM"},
        {"name": "TA LEAD"},
        {"name": "TT"},
        {"name": "IPIC"},
        {"name": "IPIC NCM"},
        {"name": "IPIC LEAD"},
        {"name": "ESPECIALIST"},
    ),

    Group: (
        {"name": "TA"},
        {"name": "TT"},
        {"name": "IPIC"},
        {"name": "IPIC NCM"},
        {"name": "ESPECIALIST"},
    ),
}


@transaction.atomic
def create_user(user_data: dict[str, Any]) -> None:
    global Department, Job, Group, ObjectDoesNotExist

    user_data["password"] = user_data.get("password", "passw0rd")
    user_data["last_name"] = user_data.get("first_name", "Test")
    user_data["last_name"] = user_data.get("last_name", "Test")
    user_data["email"] = user_data.get("email", "admin@test.com")
    user_data["department"] = user_data.get("department", Department.objects.get(pk=1))
    user_data["job"] = user_data.get("job", Job.objects.get(pk=1))

    try:
        user = User.objects.create_user(**user_data)
    except IntegrityError:
        return None

    try:
        user.groups.add(Group.objects.get(name=user.username))
    except ObjectDoesNotExist:
        pass


@transaction.atomic
def create_option(model: Type[Model], data: dict[str, Any]) -> None:
    try:
        model(**data).save()
    except IntegrityError:
        pass

def insert_data(model_list: dict[Type[Model], list[dict[str, Any]]]) -> None:
    global get_user_model, create_user, create_option, User, IntegrityError

    for model, data_list in model_list.items():
        if model == User:
            for data in data_list:
                create_user(data)

        else:
            for data in data_list:
                create_option(model, data)


insert_data(options)

users = {
    User: (
        {
            "username": "alanv",
            "first_name": "Alan",
            "last_name": "Vazquez",
            "is_superuser": True,
            "is_staff": True
        },
        {
            "username": "TA",
            "first_name": "TA",
            "department": Department.objects.get(name="PRUEBAS"),
            "job": Job.objects.get(name="TA")
        },
        {
            "username": "IPIC",
            "first_name": "IPIC",
            "department": Department.objects.get(name="CONTROL DE MATERIALES"),
            "job": Job.objects.get(name="IPIC")
        },
        {
            "username": "IPIC NCM",
            "first_name": "IPIC NCM",
            "department": Department.objects.get(name="CONTROL DE MATERIALES"),
            "job": Job.objects.get(name="IPIC NCM")
        }
    )
}

insert_data(users)
