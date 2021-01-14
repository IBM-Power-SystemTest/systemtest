from django.db import models

class AbstractOptionsModel(models.Model):
    id = models.SmallAutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ['-name']
