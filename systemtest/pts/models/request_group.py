# Django
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db import models

# APPs
from systemtest.utils import models as utils_models


class RequestGroupWorkspace(utils_models.AbstractOptionsModel):
    """
    RequestGroupWorkspace table to know the location of group of requirements
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "pts_request_group_workspace"
        verbose_name = "group workspace"
        verbose_name_plural = "group workspaces"


class RequestGroup(models.Model):
    """
    Group table to grop several requirements with common data
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        part_description:
            Name or description of part to request
        part_number:
            Part Numbers of the original requirement
        is_vpd:
            Parts that are given to change
        is_serialized:
            If Part number has serial number
        system_number:
            Or MFGN
        system_cell:
            Logic testcell where the system is
        is_loaner:
            Only if the system needs loaner parts
        qty:
            Number of pieces of the same PN
        request_group_workspace:
            Location where the system is
        request_bay:
            Cluster of user
        Meta:
            Model/table options
    """

    # Part info
    part_description = utils_models.CharFieldUpper(
        "Description",
        help_text="Name or description of part (15 chars max)",
        max_length=15,
        uppercase=True,
    )
    part_number = utils_models.CharFieldUpper(
        "Part Number [ PN ]",
        help_text="Part Numbers of the original requirement (7 chars)",
        max_length=7,
        validators=[utils_models.Validators.chars(7)],
        uppercase=True,
    )
    is_vpd = models.BooleanField(
        "VPD o TPM",
        help_text="Parts that are given to change",
        default=False,
    )
    is_serialized = models.BooleanField(
        "Serialized",
        help_text="If Part number has serial number",
        default=True,
    )
    # System info
    system_number = utils_models.CharFieldUpper(
        "System Number [ MFGN ]",
        help_text="MFGN (7 chars)",
        max_length=7,
        validators=[utils_models.Validators.chars(7)],
        uppercase=True,
    )
    system_cell = utils_models.CharFieldUpper(
        "System's testcell",
        help_text="Logic testcell where the system is (7 chars max)",
        max_length=7,
        null=True,
        blank=False,
        validators=[utils_models.Validators.chars(4)],
        uppercase=True,
    )
    # Request info
    is_loaner = models.BooleanField(
        "Loaner",
        help_text="Only if the system needs loaner parts",
        default=False,
    )
    qty = models.SmallIntegerField(
        "Quantity",
        help_text="Number of pieces of the same PN",
        default=1,
        validators=utils_models.Validators.digits(10, 1, False)
    )
    request_group_workspace = models.ForeignKey(
        to=RequestGroupWorkspace,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Location",
        help_text="Location where the system is",
    )
    request_bay = utils_models.CharFieldUpper(
        "Cluster TA",
        help_text="Cluster of user (4 chars max)",
        max_length=4,
        null=True,
        blank=False,
        validators=[utils_models.Validators.chars(4)],
        uppercase=True,
    )

    def __str__(self) -> str:
        output = (
            f"{self.system_number} "
            f"{self.system_cell} "
            f"{self.part_description}")
        return output

    class Meta:
        db_table = "pts_request_group"
        verbose_name = "group"
        verbose_name_plural = "groups"
