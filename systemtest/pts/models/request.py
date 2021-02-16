# Python
import uuid

# Django
from django.db import models
from django.urls import reverse

# APPs
from systemtest.utils import models as utils_models
from .request_group import RequestGroup


class RequestStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "pts_request_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class RequestAbstractModel(models.Model):
    request_status = models.ForeignKey(
        to=RequestStatus,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        verbose_name="Estado",
        help_text="Estado del requerimiento",
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
        default="",
        uppercase=True,
    )
    created = models.DateTimeField(
        "Creacion",
        help_text="Fecha y hora de solicitud",
        auto_now_add=True,
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
        default=""
    )

    class Meta:
        abstract = True


class Request(RequestAbstractModel):
    request_group = models.ForeignKey(
        to=RequestGroup,
        on_delete=models.PROTECT,
        verbose_name="Grupo",
        help_text="Grupo en el que se solicito",
    )
    ncm_tag = models.PositiveIntegerField(
        "NCM",
        help_text="Numero de Tag en caso de tener",
        null=True,
        blank=True,
        unique=True,
        validators=[
            utils_models.Validators.eight_digits_min,
            utils_models.Validators.eight_digits_max
        ],
    )
    modified = models.DateTimeField(
        "Actualizacion",
        help_text="Fecha y hora de ultimo cambio de estado",
        auto_now=True,
    )

    def get_history_data(self):
        fields = RequestHistory._meta.fields
        data = {"request": self}

        for field in fields:
            name = field.name
            if name == "id" or name == "created":
                continue
            if hasattr(self, name):
                value = getattr(self, name)
                data[name] = value

        return data

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        RequestHistory(**self.get_history_data()).save()

    def get_first_request(self):
        return self.request_history.earliest("created")

    def get_absolute_url(self):
        return reverse("pts:detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"{self.pk} {self.request_group}"

    class Meta:
        db_table = "pts_request"
        verbose_name = "request"
        verbose_name_plural = "requests"


class RequestHistory(RequestAbstractModel):
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
