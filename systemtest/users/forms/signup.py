from typing import Any

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.db.models import Q


from django.contrib.auth.models import Group
from systemtest.users.models import Job

User = get_user_model()


class SignUpForm(UserCreationForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
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
