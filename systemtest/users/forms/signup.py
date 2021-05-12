# Python
from typing import Any

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.db.models import Q

from django.contrib.auth.models import Group

# APPs
from systemtest.users.models import Job

User = get_user_model()


class SignUpForm(UserCreationForm):
    """
    Form to registry new users, custom options for each group, only staff
    cam register/create more users based on Django form to create users
        References:
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm

    Attributes:
        username:
            Unique username
        email:
            email, Not necessarily unique
        fist_name:
            First name
        last_name:
            Last name
        groups:
            Authentication groups to which the user belongs, when a user
            is created it is inherited from the user who creates it
        job:
            Position or role of new user
        is_staff:
            Staff permisions or role
        mfs:
            Manufactoring Floor System user if it has
        password1:
            Password that must comply with the constrains
        password2:
            Password1 confirmation
        Meta:
            Form options
    """
    def __init__(self, *args: Any, **kwargs: Any):
        """
        Changes the choices of groups and jobs according to the user's group
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        if user:
            if user_groups := user.groups.all():
                query_ipic = Q(name__icontains="IPIC")
                query_ta = (
                    Q(name__icontains="TA") |
                    Q(name="TT") |
                    Q(name="ESPECIALIST")
                )

                if user_groups.filter(query_ipic):
                    job_choices = Job.objects.filter(query_ipic)
                    group_choices = Group.objects.filter(query_ipic)
                elif user_groups.filter(query_ta):
                    group_choices = Group.objects.filter(query_ta)
                    job_choices = Job.objects.filter(query_ta)

                self.fields["groups"] = forms.ModelChoiceField(group_choices)
                self.fields["job"] = forms.ModelChoiceField(job_choices)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'job',
            'is_staff',
            'mfs',
            'password1',
            'password2',
        )
