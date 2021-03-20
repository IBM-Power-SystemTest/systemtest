# Python
import uuid

# Django
from django.db import models

# APPs
from systemtest.utils import models as utils_models


class QualityStatus(utils_models.AbstractOptionsModel):
    class Meta:
        db_table = "quality_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class QualityAbstractSystem(models.Model):
    id = models.UUIDField(
        "Identificador",
        help_text="Identificador unico [ UUID ]",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )

    system_number = utils_models.CharFieldUpper(
        "Numero de sistema",
        help_text="7 caracteres",
        max_length=7,
        unique=True,
        validators=[utils_models.Validators.chars(7)],
        uppercase=True,
    )

    workunit = utils_models.CharFieldUpper(
        "WorkUnit",
        help_text="8 caracteres",
        max_length=8,
        unique=True,
        validators=[utils_models.Validators.chars(8)],
        uppercase=True
    )

    workunit_qty = models.PositiveIntegerField(
        "WorkUnit Quantity",
        help_text="Cantidad de sistemas de la familia",
        validators=utils_models.Validators.digits(1, 50, False)
    )

    product_line = utils_models.CharFieldUpper(
        "Product Line",
        max_length=20,
        help_text="Tipo de sistema",
        uppercase=True
    )

    machine_type = models.PositiveIntegerField(
        "Machine Type",
        help_text="Numero 4 digitos",
        validators=utils_models.Validators.digits(4)
    )

    system_model = utils_models.CharFieldUpper(
        "Model",
        help_text="3 caracteres",
        max_length=3,
        validators=[utils_models.Validators.chars(3)],
        uppercase=True
    )

    operation_number = utils_models.CharFieldUpper(
        "Operation Number",
        help_text="Number of operation comming from",
        max_length=5,
        uppercase=True
    )

    operation_status = utils_models.CharFieldUpper(
        "Operation Status",
        help_text="Operation status to know if system goes to consolidation",
        max_length=1,
        uppercase=True
    )

    quality_status = models.ForeignKey(
        to=QualityStatus,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        verbose_name="Estado",
        help_text="Estado del sistema"
    )

    created = models.DateTimeField(
        "Creacion",
        help_text="Fecha y hora de creacion",
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


class QualitySystem(QualityAbstractSystem):
    modified = models.DateTimeField(
        "Actualizacion",
        help_text="Fecha y hora de ultimo cambio de estado",
        auto_now=True,
    )

    def get_history_data(self):
        fields = QualityHistory._meta.fields
        data = {"system": self}

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
        QualityHistory(**self.get_history_data()).save()

    class Meta:
        db_table = "quality_system"
        verbose_name = "system"
        verbose_name_plural = "systems"


class QualityHistory(QualityAbstractSystem):
    system = models.ForeignKey(
        to=QualitySystem,
        on_delete=models.PROTECT,
        verbose_name="Requerimiento",
        help_text="Numero del requerimiento original, con el estado actual",
        related_name="request_history"
    )

    class Meta:
        db_table = "quality_history"
        verbose_name = "history"
        verbose_name_plural = "history"
