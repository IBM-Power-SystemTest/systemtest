from typing import Any, Type
import subprocess
import csv

from django.contrib.auth.models import Group
from systemtest.users.models import Job, Department

from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

passwd = "./systemtest/utils/passwd"


def run_cmd(cmd, *args, **kwargs):
    return subprocess.run(
        cmd,
        capture_output=True,
        shell=True,
        text=True
    )


def get_fields(user):
    cmd_grep_user = f"grep ^{user}: {passwd}"

    grep_user = run_cmd(cmd_grep_user).stdout
    if not grep_user:
        return "", "", ""
    grep_user = grep_user.split("/")

    fullname = grep_user[4].split()
    email = grep_user[5].split(":")[0].lower()

    if "nahumra" in email:
        first_names = " ".join(fullname[2:]).title()
        last_names = " ".join(fullname[:2]).title()
    else:
        first_names = " ".join(fullname[:-2]).title()
        last_names = " ".join(fullname[-2:]).title()

    return first_names, last_names, email


def add_fields(inputpath, outputpath="output.csv"):
    with open(inputpath, 'r') as csvinput:
        inputrows = csv.DictReader(csvinput)
        with open(outputpath, 'w') as csvoutput:
            new_fields = ["first_name", "last_name", "email", "password"]
            fieldnames = inputrows.fieldnames + new_fields
            writer = csv.DictWriter(csvoutput, fieldnames=fieldnames)

            writer.writeheader()
            for i, row in enumerate(inputrows):
                user = row["username"]
                first_name, last_name, email = get_fields(user)

                row[new_fields[0]] = first_name
                row[new_fields[1]] = last_name
                row[new_fields[2]] = email
                row[new_fields[3]] = f"ptspass{i:02x}"

                writer.writerow(row)


def get_rows(filepath):
    with open(filepath, "r") as f:
        for row in csv.DictReader(f):
            yield row


def set_index(data, key, list):
    i = int(data[key])
    data[key] = list[i]


def create_users(filepath):
    departments = Department.objects.all()
    jobs = Job.objects.all()
    groups = Group.objects.all()

    for i, row in enumerate(get_rows(filepath)):
        set_index(row, "job", jobs)
        set_index(row, "department", departments)
        set_index(row, "group", groups)
        row["is_staff"] = int(row["is_staff"])

        print(row)
        create_user(row)


def create_user(user_data: dict[str, Any]) -> None:
    group = user_data.pop("group")
    try:
        user = User.objects.create_user(**user_data)
    except IntegrityError:
        return None

    try:
        user.groups.add(Group.objects.get(name=group))
    except ObjectDoesNotExist:
        pass


if __name__ == "__main__":
    inputpath = "./systemtest/utils/users.csv"
    outputpath = "./systemtest/utils/users_new.csv"

    add_fields(inputpath, outputpath)
    # create_users(outputpath)

    # exec(open('systemtest/utils/load_users.py').read())
