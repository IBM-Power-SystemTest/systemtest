# Python
import uuid

# Django
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# APPs
from systemtest.utils import models as utils_models


class PeopleType(utils_models.AbstractOptionsModel):
    """
    People table for requirement types
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "people_type"
        verbose_name = "type"
        verbose_name_plural = "types"


class PeopleStatus(utils_models.AbstractOptionsModel):
    """
    People table for requirement status
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "people_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class AbstractPeopleRequirement(models.Model):
    status = models.ForeignKey(
        PeopleStatus,
        models.PROTECT,
        default=1,
        verbose_name="Activity Type",
        help_text="Type of activity to be assigned",
    )
    comment = utils_models.CharFieldUpper(
        "Comment",
        help_text="Additional coment",
        max_length=50,
        blank=True,
        null=True,
        default=None
    )
    start = models.DateField(
        "Start",
        help_text="Start Date",
        default=now
    )
    days = models.SmallIntegerField(
        "Days",
        help_text="Number of days that are granted with the requirement",
        default=1,
    )
    created = models.DateTimeField(
        "Created",
        help_text="Request DateTime",
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class PeopleRequirement(AbstractPeopleRequirement):
    type = models.ForeignKey(
        PeopleType,
        models.PROTECT,
        default=1,
        verbose_name="Requirement Type",
        help_text="Type of requirement to be assigned"
    )
    by_user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Requested by",
        help_text="User who makes the request",
        related_name="by_user_set"
    )
    for_user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Requested for",
        help_text="User who receives the request",
        related_name="for_user_set"
    )
    description = utils_models.CharFieldUpper(
        "Description",
        help_text="Description about the requirement",
        max_length=30,
        uppercase=False,
        null=True,
        blank=True,
        default=None
    )
    modified = models.DateTimeField(
        "Updated",
        help_text="Update DateTime",
        auto_now=True,
    )

    def get_history_data(self):
        # Gets fields from RequestHistory
        fields = PeopleHistory._meta.fields

        # Base field is ForeignKey to System instance
        data = {"requirement": self}

        for field in fields:
            # Get field name
            name = field.name

            # Field to unfetch
            if name == "created" or name == "id":
                continue

            # Check if System instance has the field name
            if hasattr(self, name):

                # Saving the System instance in QualityHistory data
                value = getattr(self, name)
                data[name] = value

        return data

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        PeopleHistory(**self.get_history_data()).save()

    def get_absolute_url(self) -> str:
        """
        To create a unique url for each System used to modify only this System
        Use a url 'quality:system_detail'='/quality/system_detail/<pk>' parsing the pk [workunit] of system on the args
            References:
                https://docs.djangoproject.com/en/3.1/ref/models/instances/#get-absolute-url

        Args:
            self:
                QualitySystem intance.

        Returns:
            str for parsed URL

            example:
                '/quality/system_detail/3BDRZJSR/'
        """

        return reverse("people:requirement_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"{self.for_user}:{self.type}"

    class Meta:
        db_table = "people_requirement"
        verbose_name = "requirement"
        verbose_name_plural = "requirements"


class PeopleHistory(AbstractPeopleRequirement):
    id = models.UUIDField(
        "UID",
        help_text="Unique Identifier [ UUID ]",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    requirement = models.ForeignKey(
        to=PeopleRequirement,
        on_delete=models.PROTECT,
        verbose_name="Requirement",
        help_text="Current requirement",
    )

    class Meta:
        db_table = "people_requirement_history"
        verbose_name = "history"
        verbose_name_plural = "history"
