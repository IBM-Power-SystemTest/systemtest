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
    system_number = utils_models.CharFieldUpper(
        "Numero de sistema",
        help_text="7 caracteres",
        max_length=7,
        validators=[utils_models.Validators.seven_chars],
        uppercase=True,
    )

    workunit = utils_models.CharFieldUpper(
        "WorkUnit",
        help_text="8 caracteres",
        max_length=8,
        validators=[utils_models.Validators.eight_chars],
        uppercase=True
    )

    product_line = utils_models.CharFieldUpper(
        "Product Line",
        help_text="Tipo de sistema",
        uppercase=True
    )

    machine_type = models.PositiveIntegerField(
        "Machine Type",
        help_text="Numero 4 digitos",
        validators=[
            utils_models.Validators.four_digits_min,
            utils_models.Validators.four_digits_max
        ]
    )

    system_model = utils_models.CharFieldUpper(
        "Model",
        help_text="3 caracteres",
        max_length=3,
        validators=[utils_models.Validators.three_chars],
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
        verbose_name = "quality"
        verbose_name_plural = "qualities"


class QualityHistory(QualityAbstractSystem):
    id = models.UUIDField(
        "Identificador",
        help_text="Identificador unico [ UUID ]",
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )

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
