# Python
import uuid

# Django
from django.db import models
from django.urls import reverse

# APPs
from systemtest.utils import models as utils_models
from .request_group import RequestGroup


class RequestStatus(utils_models.AbstractOptionsModel):
    """
    RequestStatus table to know status of each requirement
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "pts_request_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class RequestAbstractModel(models.Model):
    """
    Abstract model for Request tables (Request and RequestHistory)
    group common fields between these tables
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        request_status:
            Requirement status
        part_number:
            Part Number
        serial_number:
            Serial Number
        created:
            Creation DateTime
        user:
            User who made the insert or update
        comment:
            Addition comment
        Meta:
            Model/table options
    """

    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        verbose_name="Status",
        help_text="Requirement status",
    )
    part_number = utils_models.CharFieldUpper(
        "Part Number [ PN ]",
        help_text="Part Number (7 chars)",
        max_length=7,
        validators=[utils_models.Validators.chars(7)],
        uppercase=True,
    )
    serial_number = utils_models.CharFieldUpper(
        "Serial Number [ SN ]",
        help_text="Serial Number [optional] (12 chars)",
        max_length=12,
        validators=[utils_models.Validators.chars(12)],
        null=True,
        blank=True,
        default=None,
        uppercase=True,
    )
    created = models.DateTimeField(
        "Created",
        help_text="Request DateTime",
        auto_now_add=True,
    )
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="User",
        help_text="User who made the last transaction",
    )
    comment = utils_models.CharFieldUpper(
        "Coment",
        help_text="Aditional comment",
        max_length=30,
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True


class Request(RequestAbstractModel):
    """
    Request table based on the RequestAbstractModel adding extra fields
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        request_group:
            Request Group to grouping several Requirements, changing the Serial Number mainly
        nam_tag:
            Only used when the requeriment is returned as bad
        modified:
            Updated DateTime
        Meta:
            Model/table options
    """

    request_group = models.ForeignKey(
        to=RequestGroup,
        on_delete=models.PROTECT,
        verbose_name="Group",
        help_text="Reqeust Group",
    )
    ncm_tag = models.PositiveIntegerField(
        "NCM",
        help_text="Non-Conforming Material (8 numeric chars)",
        null=True,
        blank=True,
        unique=True,
        default=None,
        validators=utils_models.Validators.digits(8)
    )
    modified = models.DateTimeField(
        "Updated",
        help_text="Updated DateTime",
        auto_now=True,
    )

    def get_history_data(self) -> dict:
        """
        Gets a data necesary for RequestHistory object looking for common fields

        Args:
            self:
                Request intance.

        Returns:
            A dict mapping keys to the corresponding field for RequestHistory table

            example:
                {
                    request_status: <RequestStatus: CLOSE BAD>,
                    part_number: "78P4198"
                    serial_number: "YH10M9030S90"
                    created: datetime.datetime(2021, 4, 5, 7, 45, 25, 324317),
                    user: <User: alanv>,
                    comment: "",
                }
        """

        # Gets fields from RequestHistory
        fields = RequestHistory._meta.fields

        # Base field is ForeignKey to Request instance
        data = {"request": self}

        for field in fields:
            # Get field name
            name = field.name

            # Field to unfetch
            if name == "id" or name == "created":
                continue

            # Check if Request instance has the field name
            if hasattr(self, name):

                # Saving the Request instance in RequestHistory data
                value = getattr(self, name)
                data[name] = value

        return data

    def save(self, *args, **kwargs) -> None:
        """
        After normal save create a RequestHistory instance and save in database

            reference:
                https://docs.djangoproject.com/en/3.1/ref/models/instances/#django.db.models.Model.save

        Args:
            self:
                Request intance.

        Returns:
            None
        """
        super().save(*args, **kwargs)

        # Saving the update or creation Request on a history table (RequestHistory)
        RequestHistory(**self.get_history_data()).save()

    def get_first_request(self):
        """
        Fetchs the first Request saved from RequestHistory model (table)
        Using the request ForeignKey related_name (request_history) set of history requests
            References:
                https://docs.djangoproject.com/en/3.1/topics/db/queries/#backwards-related-objects
                https://docs.djangoproject.com/en/3.1/ref/models/querysets/#earliest

        Args:
            self:
                Request intance.

        Returns:
            RequestHistory object the earliest by creation, the first one

            example:
                <RequestHistory: 1 BBCGL22 B262 DIMM YH10MS032140 OPEN 2021-04-05 07:45:25.326357 alanv>
        """

        return self.request_history.earliest("created")

    def get_absolute_url(self) -> str:
        """
        To create a unique url for each Request used to cancel or modify only this Request
        Use a url 'pts:detail'='/pts/detail/<pk>' parsing the pk of Request on the args
            References:
                https://docs.djangoproject.com/en/3.1/ref/models/instances/#get-absolute-url

        Args:
            self:
                Request intance.

        Returns:
            str for parsed URL

            example:
                '/pts/request/1/'
        """

        return reverse("pts:detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"{self.pk} {self.request_group}"

    class Meta:
        db_table = "pts_request"
        verbose_name = "request"
        verbose_name_plural = "requests"


class RequestHistory(RequestAbstractModel):
    """
    RequestHistory table based on the RequestAbstractModel adding extra fields
    This table is used for save all change in one original request
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        id:
            Change the base pk (interger) to UUID for have most rows
        request:
            ForeignKey to original request One Request and Many History rows
        Meta:
            Model/table options
    """
    id = models.UUIDField(
        "UID",
        help_text="Unique Identifier [ UUID ]",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    request = models.ForeignKey(
        to=Request,
        on_delete=models.PROTECT,
        verbose_name="Requirement",
        help_text="Original Requirement",
        related_name="request_history"
    )

    def __str__(self) -> str:
        output = (
            f"{self.request} "
            f"{self.serial_number} "
            f"{self.request_status} "
            f"{self.created} "
            f"{self.user}"
        )
        return output

    class Meta:
        db_table = "pts_request_history"
        verbose_name = "history"
        verbose_name_plural = "history"
