# Python
import uuid

# Django
from django.db import models

# APPs
from systemtest.utils import models as utils_models


class RequestGroupStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_status"
        verbose_name = "group status"
        verbose_name_plural = "group status"


class RequestGroupWorkspace(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_group_workspace"
        verbose_name = "group workspace"
        verbose_name_plural = "group workspaces"


class RequestGroup(models.Model):
    # Part info
    part_description = utils_models.CharFieldUpper(
        "Descripcion",
        help_text="Nombre de la pieza/parte",
        max_length=15,
        uppercase=True,
    )
    part_number = utils_models.CharFieldUpper(
        "Part Number [ PN ]",
        help_text="Numero de parte(s) del requerimiento original",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    is_vpd = models.BooleanField(
        "VPD o TPM",
        help_text="Se entrega al cambio",
        default=False,
    )
    is_serialized = models.BooleanField(
        "Serializado",
        help_text="Numero de parte con serial",
        default=True,
    )
    # System info
    system_number = utils_models.CharFieldUpper(
        "Numero de sistema",
        help_text="7 caracteres",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    system_cell = utils_models.CharFieldUpper(
        "Celda del sistema",
        help_text="4 caracteres o mas",
        max_length=7,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
    )
    # Request info
    is_loaner = models.BooleanField(
        "Loaner",
        help_text="El sistema require que las piezas sean 'Loaner'",
        default=False,
    )
    qty = models.SmallIntegerField(
        "Cantidad", help_text="Cantidad de piezas del mismo PN", default=1
    )
    request_group_workspace = models.ForeignKey(
        to=RequestGroupWorkspace,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Area",
        help_text="El area donde esta el sistema",
    )
    request_group_status = models.ForeignKey(
        to=RequestGroupStatus,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Estado del grupo",
        help_text="Representa el estado de la piezas de este grupo",
    )
    request_bay = utils_models.CharFieldUpper(
        "Bahia TA",
        help_text="4 caracteres",
        max_length=4,
        null=True,
        blank=False,
        validators=[utils_models.Validators.four_chars],
        uppercase=True,
    )

    def __str__(self) -> str:
        output = f"{self.system_number} " f"{self.system_cell} " f"{self.part_number}"
        return output

    class Meta:
        db_table = "pts_request_group"
        verbose_name = "group"
        verbose_name_plural = "groups"


class RequestStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class RequestNotNcmStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_not_ncm"
        verbose_name = "reason for no ncm"
        verbose_name_plural = "reason for no ncm"


class Request(models.Model):
    request_group = models.ForeignKey(
        to=RequestGroup,
        on_delete=models.PROTECT,
        verbose_name="Grupo",
        help_text="Grupo en el que se solicito",
    )
    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        default=1,
        verbose_name="Estado",
        help_text="Estado del requerimiento",
    )
    ncm_tag = models.PositiveIntegerField(
        "NCM",
        help_text="Numero de Tag en caso de tener",
        null=True,
        blank=True,
        unique=True,
        validators=[utils_models.Validators.nine_digits],
    )
    not_ncm_status = models.ForeignKey(
        to=RequestNotNcmStatus,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Motivos de tag faltante",
        help_text="En caso que el estado sea malo, pero no se haya generado Tag",
    )
    part_number = utils_models.CharFieldUpper(
        "Numero de parte [ PN ]",
        help_text="7 caracteres, rellenar con 0's",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    serial_number = utils_models.CharFieldUpper(
        "Numero de Seria [ SN ]",
        help_text="12 caracteres",
        max_length=12,
        validators=[utils_models.Validators.twelve_chars],
        null=True,
        blank=True,
        uppercase=True,
    )
    created = models.DateTimeField(
        verbose_name="Creacion",
        help_text="Fecha y hora de solicitud",
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        "Actualizacion",
        help_text="Fecha y hora de ultimo cambio de estado",
        auto_now=True,
    )
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Usuario",
        help_text="Usuario que realizo el cambio de estado",
    )
    comment = utils_models.CharFieldUpper(
        "Comentario",
        help_text="Comentario adicional en estado actual",
        max_length=30,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.request_group}"

    class Meta:
        db_table = "pts_request"
        verbose_name = "request"
        verbose_name_plural = "requests"


class RequestHistory(models.Model):
    id = models.UUIDField(
        "Identificador",
        help_text="Identificador unico [ UUID ]",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    request = models.ForeignKey(
        to=Request,
        on_delete=models.PROTECT,
        verbose_name="Requerimiento",
        help_text="Numero del requerimiento original, con el estado actual",
    )
    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        verbose_name="Estado",
        help_text="Estado del requerimiento orginal",
    )
    part_number = utils_models.CharFieldUpper(
        "Numero de parte [ PN ]",
        help_text="PN del requerimiento original",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )
    serial_number = utils_models.CharFieldUpper(
        "Numero de Seria [ SN ]",
        help_text="SN del requerimiento original",
        max_length=12,
        validators=[utils_models.Validators.twelve_chars],
        null=True,
        blank=True,
        uppercase=True,
    )
    created = models.DateTimeField(
        "Creacion",
        help_text="Fecha y hora del cambio de estado del requerimineto original",
        auto_now_add=True,
    )
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name="Usuario",
        help_text="Usuario que realizo el cambio de estado en el requerimiento original",
    )
    comment = utils_models.CharFieldUpper(
        "Comentario",
        help_text="Comantario en estado del requerimineto",
        max_length=30,
        blank=True,
        null=True,
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
        db_table = "pts_request_track"
        verbose_name = "history"
        verbose_name_plural = "history"
