# Django
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db import models

# APPs
from systemtest.utils import models as utils_models


class RequestGroupWorkspace(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_workspace"
        verbose_name = "group workspace"
        verbose_name_plural = "group workspaces"


class RequestGroup(models.Model):
    # Part info
    part_description = utils_models.CharFieldUpper(
        "Descripcion",
        help_text="Nombre o descripcion de la pieza/parte (15 caracteres maximo)",
        max_length=15,
        uppercase=True,
    )
    part_number = utils_models.CharFieldUpper(
        "Part Number [ PN ]",
        help_text="Numero de parte(s) del requerimiento original (7 caracteres)",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    is_vpd = models.BooleanField(
        "VPD o TPM",
        help_text="Son piezas que se entregan al cambio",
        default=False,
    )
    is_serialized = models.BooleanField(
        "Serializado",
        help_text="""Numero de parte con serial.
            Si no tiene serial solo es necesario registrar un numero de parte.
            Los seriales solo pueden pertenecer a un numero de parte""",
        default=True,
    )
    # System info
    system_number = utils_models.CharFieldUpper(
        "Numero de sistema",
        help_text="MFGN. Familia del Sistema (7 caracteres)",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    system_cell = utils_models.CharFieldUpper(
        "Celda del sistema",
        help_text="Celda logica donde esta el sistema (7 caracteres maximo)",
        max_length=7,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
    )
    # Request info
    is_loaner = models.BooleanField(
        "Loaner",
        help_text="""El sistema necesita piezas 'Loaner'.
            Solo se debe usar cuando no deje reemplazar piezas normales""",
        default=False,
    )
    qty = models.SmallIntegerField(
        "Cantidad",
        help_text="Cantidad de piezas del mismo PN",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    request_group_workspace = models.ForeignKey(
        to=RequestGroupWorkspace,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Area",
        help_text="El area donde esta el sistema",
    )
    request_bay = utils_models.CharFieldUpper(
        "Bahia TA",
        help_text="Bahia del usuario que requiere la pieaza (4 caracteres maximo)",
        max_length=4,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
    )

    def get_absolute_url(self):
        return reverse("pts:detail_group", args=[str(self.pk)])

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
