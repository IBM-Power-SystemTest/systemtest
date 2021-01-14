import uuid
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from systemtest.utils import models as utils_models


class RequestGroupStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_status"


class RequestGroupWorkspace(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_workspace"


class RequestGroup(models.Model):
    validate = {
        "seven_chars": RegexValidator(r"^[a-zA-Z0-9]{7}$"),
        "four_chars": RegexValidator(r"^[a-zA-z0-9]{4}$")
    }

    # Part info
    part_description = models.CharField(max_length=15)
    part_number = models.CharField(
        max_length=7,
        validators=[validate["seven_chars"]]
    )
    is_vpd = models.BooleanField(default=False)
    is_serialized = models.BooleanField(default=True)
    # System info
    system_number = models.CharField(
        max_length=7,
        validators=[validate["seven_chars"]]
    )
    system_cell = models.CharField(
        max_length=4,
        null=True,
        blank=False,
        validators=[validate["four_chars"]]
    )
    # Request info
    is_loaner = models.BooleanField(default=False)
    qty = models.SmallIntegerField(default=1)
    request_group_workspace = models.ForeignKey(
        to=RequestGroupWorkspace,
        on_delete=models.PROTECT,
        default=1
    )
    request_group_status = models.ForeignKey(
        to=RequestGroupStatus,
        on_delete=models.PROTECT,
        default=1
    )
    request_bay = models.CharField(
        max_length=4,
        null=True,
        blank=False,
        validators=[validate["four_chars"]]
    )

    def __str__(self) -> str:
        output = (
            f"{self.system_number} "
            f"{self.system_cell} "
            f"{self.part_number}"
        )
        return output

    class Meta:
        db_table = "pts_request_group"


class RequestStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_status"

class RequestNotNcmStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_not_ncm"

class Request(models.Model):
    request_group = models.ForeignKey(
        to=RequestGroup,
        on_delete=models.PROTECT,
    )
    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        default=1
    )
    ncm_tag = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
        validators=[MaxValueValidator(int("9"*8))]
    )
    not_ncm_status = models.ForeignKey(
        to=RequestNotNcmStatus,
        on_delete=CASCADE,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f"{self.request_group}"

    class Meta:
        db_table = "pts_request"


class RequestTrackStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_track_status"


class RequestTrackDelayStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_track_delay_status"

class RequestTrack(models.Model):
    validate = {
        "twelve_chars": RegexValidator(r"^[a-zA-Z0-9]{12}$"),
        "seven_chars": RegexValidator(r"^[a-zA-Z0-9]{7}$")
    }

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    request = models.ForeignKey(
        to=Request,
        on_delete=models.PROTECT
    )
    request_track_status = models.ForeignKey(
        to=RequestTrackStatus,
        on_delete=models.PROTECT,
        default=1
    )
    part_number = models.CharField(
        max_length=7,
        validators=[validate["seven_chars"]]
    )
    serial_number = models.CharField(
        max_length=12,
        validators=[validate["twelve_chars"]],
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT
    )
    delay_status = models.ForeignKey(
        to=RequestTrackDelayStatus,
        on_delete=PROTECT,
        null=True,
        blank=True
    )
    comment = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        default=""
    )

    def __str__(self) -> str:
        output = (
            f"{self.request} {self.serial_number} "
            f"{self.request_track_status} {self.created} "
            f"{self.user}"
        )
        return output

    class Meta:
        db_table = "pts_request_track"
