# Python
import uuid

# Django
from django.db import models
from django.urls.base import reverse
from django.core.exceptions import ObjectDoesNotExist

# APPs
from systemtest.utils import models as utils_models


class QualityStatus(utils_models.AbstractOptionsModel):
    """
    QualityStatus table to know the status of the system
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        Meta:
            Model/table options
    """

    class Meta:
        db_table = "quality_status"
        verbose_name = "status"
        verbose_name_plural = "status"


class AbstractQualitySystem(models.Model):
    """
    Abstract model for Quality Systems tables (QualitySystem and QualityHistoy)
    group common fields between these tables
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        operation_number:
            Number of operation is
        operation_status:
            Operation status to know if system goes to consolidation
        quality_status:
            Indicates the system status
        created:
            Creation DateTime
        user:
            User who made the insert or update
        comment:
            Addition comment
        Meta:
            Model/table options
    """

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
        null=True,
        blank=True,
        verbose_name="Status",
        help_text="System status"
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
        null=True,
        blank=True,
        default=None,
    )

    comment = utils_models.CharFieldUpper(
        "Comentario",
        help_text="Comentario adicional en estado actual",
        max_length=30,
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True


class QualitySystem(AbstractQualitySystem):
    """
    QualitySystem table based on the QualityAbstractSystem adding extra fields
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        system_number:
            MFGN
        workunit:
            WU also setted as PK (ID)
        workunit_qty:
            Quantity of system that are on the same MFGN
        product_line:
            System type
        modified:
            DateTime from the last update
        Meta:
            Model/table options
    """

    system_number = utils_models.CharFieldUpper(
        "System Number [ MFGN ]",
        help_text="MFGN (7 chars)",
        max_length=7,
        validators=[utils_models.Validators.chars(7)],
        uppercase=True,
    )

    workunit = utils_models.CharFieldUpper(
        "WorkUnit",
        help_text="WU (8 chars)",
        primary_key=True,
        max_length=8,
        unique=True,
        validators=[utils_models.Validators.chars(8)],
        uppercase=True
    )

    workunit_qty = models.PositiveIntegerField(
        "WorkUnit Quantity",
        help_text="Quantity from same MFGN",
        null=True,
        blank=True,
        default=1,
        validators=utils_models.Validators.digits(1, 50, False)
    )

    product_line = utils_models.CharFieldUpper(
        "Product Line",
        max_length=20,
        help_text="System type",
        uppercase=True
    )

    modified = models.DateTimeField(
        "Updated",
        help_text="DateTime from last change",
        auto_now=True,
    )

    def get_history_data(self):
        """
        Gets a data necesary for QualityHistory object looking for common fields

        Args:
            self:
                Request intance.

        Returns:
            A dict mapping keys to the corresponding field for QualityHistory table

            example:
                {
                    'system': <QualitySystem: 1AU9LT7 => 3BDR2JCD>,
                    'operation_number': '0850',
                    'operation_status': 'W',
                    'quality_status': <QualityStatus: WAITING>,
                    'user': <User: alanv>,
                    'comment': None
                }
        """

        # Gets fields from RequestHistory
        fields = QualityHistory._meta.fields

        # Base field is ForeignKey to System instance
        data = {"system": self}

        for field in fields:
            # Get field name
            name = field.name

            # Field to unfetch
            if name == "created":
                continue

            # Check if System instance has the field name
            if hasattr(self, name):

                # Saving the System instance in QualityHistory data
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

        # Checking if QualitySystem has previus status if fail status is None
        try:
            old_status = QualitySystem.objects.get(pk=self.pk).quality_status
            old_operation_status = QualitySystem.objects.get(pk=self.pk).operation_status
        except ObjectDoesNotExist:
            old_status = None
            old_operation_status = None

        # If status is different than previus status save in history
        if (old_status is None) or (old_status != self.quality_status) or (old_operation_status != self.operation_status):
            QualityHistory(**self.get_history_data()).save()
            super().save(*args, **kwargs)

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

        return reverse("quality:system_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"{self.system_number} => {self.workunit}"

    class Meta:
        db_table = "quality_system"
        verbose_name = "system"
        verbose_name_plural = "systems"


class QualityHistory(AbstractQualitySystem):
    """
    QualityHistory table based on the QualityAbstractSystem adding extra
    fields. This table is used for save all change in one original system
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/models/
            https://docs.djangoproject.com/en/3.1/ref/models/options/

    Attributes:
        id:
            Change the base pk (interger) to UUID for have most rows
        request:
            ForeignKey to original system One System and Many History rows
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

    system = models.ForeignKey(
        to=QualitySystem,
        on_delete=models.PROTECT,
        verbose_name="System",
        help_text="Original system",
        related_name="system_history"
    )

    class Meta:
        db_table = "quality_history"
        verbose_name = "history"
        verbose_name_plural = "history"
