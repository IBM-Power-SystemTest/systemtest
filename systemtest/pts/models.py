import uuid

from django.core.validators import MaxValueValidator
from django.db import models

from systemtest.utils import models as utils_models


class RequestGroupStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_status"


class RequestGroupWorkspace(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_workspace"


class RequestGroup(models.Model):
    # Part info
    part_description = utils_models.CharFieldUpper(
        max_length=15,
        uppercase=True
    )
    part_number = utils_models.CharFieldUpper(
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    is_vpd = models.BooleanField(default=False)
    is_serialized = models.BooleanField(default=True)
    # System info
    system_number = utils_models.CharFieldUpper(
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    system_cell = utils_models.CharFieldUpper(
        max_length=4,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
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
    request_bay = utils_models.CharFieldUpper(
        max_length=4,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
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
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    part_number = utils_models.CharFieldUpper(
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    serial_number = utils_models.CharFieldUpper(
        max_length=12,
        validators=[utils_models.Validators.twelve_chars],
        null=True,
        blank=True,
        uppercase=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT
    )
    comment = utils_models.CharFieldUpper(
        max_length=30,
        blank=True,
        null=True,
        default=""
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.request_group}"

    class Meta:
        db_table = "pts_request"


class RequestHistory(models.Model):
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
    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        default=1
    )
    part_number = utils_models.CharFieldUpper(
        max_length=7,
        uppercase=True,
    )
    serial_number = utils_models.CharFieldUpper(
        max_length=12,
        null=True,
        blank=True,
        uppercase=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT
    )
    comment = utils_models.CharFieldUpper(
        max_length=30,
        blank=True,
        null=True,
        default=""
    )

    def __str__(self) -> str:
        output = (
            f"{self.request} {self.serial_number} "
            f"{self.request_status} {self.created} "
            f"{self.user}"
        )
        return output

    class Meta:
        db_table = "pts_request_track"
