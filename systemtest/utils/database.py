from typing import Any, Type
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError

from django.db.models import Model


from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from systemtest.users.models import Job, Departament
from systemtest.pts.models import RequestGroupWorkspace, RequestNotNcmStatus, RequestStatus

User = get_user_model()


options = {
    RequestGroupWorkspace: (
        {"name": "P/I SERIES"},
        {"name": "EARLY BUILD"},
        {"name": "CSC"},
    ),

    RequestStatus: (
        {"name": "OPEN"},
        {"name": "TRANSIT"},
        {"name": "RECIVE"},
        {"name": "RETURN"},
        {"name": "PENDING"},
        {"name": "CLOSE"},
        {"name": "CANCEL"},
        {"name": "GOOD"},
        {"name": "BAD"},
        {"name": "VALIDANDO INVENTARIO"},
        {"name": "SOLICITADO A OTRA AREA"},
        {"name": "CORTO REAL"},
        {"name": "SOLICITADO A DE GEODIS"},
        {"name": "NUMERO DE PARTE NO EXISTE"},
    ),

    RequestNotNcmStatus: (
        {"name": "INSTALADO EN OTRA WU"},
        {"name": "REVISION CON EL ME"},
    ),

    Departament: (
        {"name": "PRUEBAS"},
        {"name": "CONTROL DE MATERIALES"},
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
    ),

    Group: (
        {"name": "TA"},
        {"name": "TT"},
        {"name": "IPIC"},
        {"name": "IPIC NCM"},
    ),
}


def create_user(user_data: dict[str, Any]) -> None:
    global Departament, Job, Group, ObjectDoesNotExist

    user_data["password"] = user_data.get("password", "passw0rd")
    user_data["last_name"] = user_data.get("first_name", "Test")
    user_data["last_name"] = user_data.get("last_name", "Test")
    user_data["email"] = user_data.get("email", "admin@test.com")
    user_data["department"] = user_data.get("department", Departament.objects.get(pk=1))
    user_data["job"] = user_data.get("job", Job.objects.get(pk=1))

    try:
        user = User.objects.create_user(**user_data)
    except IntegrityError:
        return None

    try:
        user.groups.add(Group.objects.get(name=user.username))
    except ObjectDoesNotExist:
        pass


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
                try:
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
            "department": Departament.objects.get(name="PRUEBAS"),
            "job": Job.objects.get(name="TA")
        },
        {
            "username": "IPIC",
            "first_name": "IPIC",
            "department": Departament.objects.get(name="CONTROL DE MATERIALES"),
            "job": Job.objects.get(name="IPIC")
        },
        {
            "username": "IPIC NCM",
            "first_name": "IPIC NCM",
            "department": Departament.objects.get(name="CONTROL DE MATERIALES"),
            "job": Job.objects.get(name="IPIC NCM")
        }
    )
}

insert_data(users)
